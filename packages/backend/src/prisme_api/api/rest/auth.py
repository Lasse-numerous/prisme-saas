"""Authentication routes using Authentik Flow Executor API.

Custom auth UX: the frontend drives Authentik flows through these endpoints.
GitHub OAuth goes directly to GitHub (bypasses Authentik UI).
"""

from __future__ import annotations

import logging
import os
import secrets
from typing import Annotated
from urllib.parse import urlencode

import httpx
import redis.asyncio as redis
from fastapi import APIRouter, Cookie, Depends, HTTPException, Query, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from prisme_api.auth.config import authentik_settings
from prisme_api.auth.dependencies import CurrentActiveUser, create_session_jwt
from prisme_api.auth.flow_executor import FlowExecutorClient, FlowExecutorError
from prisme_api.database import get_db
from prisme_api.models.user import User
from prisme_api.schemas.auth import UserResponse
from prisme_api.schemas.auth_flow import (
    FlowChallenge,
    FlowStartResponse,
    FlowStepResponse,
    FlowSubmitRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

# Redis client for flow session storage
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
_redis_client: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    """Get or create Redis client."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client


async def get_flow_executor() -> FlowExecutorClient:
    """Get a FlowExecutorClient instance."""
    r = await get_redis()
    return FlowExecutorClient(r)


def _set_session_cookie(response: Response, token: str) -> None:
    """Set the JWT session cookie on a response."""
    response.set_cookie(
        key=authentik_settings.session_cookie_name,
        value=token,
        max_age=authentik_settings.session_max_age,
        httponly=True,
        secure=True,
        samesite="lax",
    )


def _clear_session_cookie(response: Response) -> None:
    """Clear the session cookie."""
    response.delete_cookie(
        key=authentik_settings.session_cookie_name,
        httponly=True,
        secure=True,
        samesite="lax",
    )


async def _find_or_create_user(
    db: AsyncSession,
    *,
    authentik_id: str | None = None,
    email: str,
    username: str | None = None,
    roles: list[str] | None = None,
) -> User:
    """Find an existing user by authentik_id or email, or create a new one."""
    user = None

    if authentik_id:
        result = await db.execute(select(User).where(User.authentik_id == authentik_id))
        user = result.scalar_one_or_none()

    if not user:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

    if user:
        return user

    # Validate email domain
    try:
        from prisme_api.services.allowed_email_domain import AllowedEmailDomainService

        domain_service = AllowedEmailDomainService(db)
        if not await domain_service.is_domain_allowed(email):
            domain = email.split("@")[1] if "@" in email else "unknown"
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Email domain '{domain}' is not allowed for signup. Contact admin for access.",
            )
    except ImportError:
        pass

    user = User(
        authentik_id=authentik_id or "",
        email=email,
        username=username or email.split("@")[0],
        is_active=True,
        roles=roles or ["user"],
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# ── Flow endpoints ──────────────────────────────────────────────


@router.post("/flow/login/start", response_model=FlowStartResponse)
async def flow_login_start(
    executor: Annotated[FlowExecutorClient, Depends(get_flow_executor)],
) -> FlowStartResponse:
    """Start the login authentication flow."""
    try:
        flow_token, challenge = await executor.start_flow(
            authentik_settings.login_flow_slug,
        )
        return FlowStartResponse(
            flow_token=flow_token,
            challenge=FlowChallenge(**challenge),
        )
    except FlowExecutorError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.post("/flow/login/submit", response_model=FlowStepResponse)
async def flow_login_submit(
    body: FlowSubmitRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    executor: Annotated[FlowExecutorClient, Depends(get_flow_executor)],
) -> FlowStepResponse:
    """Submit data to the login flow. On completion, issues a JWT session cookie."""
    try:
        result = await executor.submit_flow(
            body.flow_token,
            authentik_settings.login_flow_slug,
            body.data,
        )
    except FlowExecutorError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e

    if result.get("error"):
        return FlowStepResponse(
            completed=False,
            error=result["error"],
            challenge=FlowChallenge(**result["challenge"]) if result.get("challenge") else None,
        )

    if result.get("completed"):
        # Flow complete — find/create local user and issue JWT
        # We need to get user info from Authentik after flow completion
        # The flow data in 'data' should contain uid_field (email/username)
        email = body.data.get("uid_field", body.data.get("email", ""))
        user = await _find_or_create_user(db, email=email)

        token = create_session_jwt(user)
        _set_session_cookie(response, token)

        return FlowStepResponse(
            completed=True,
            user=UserResponse.model_validate(user).model_dump(),
        )

    # Next challenge
    return FlowStepResponse(
        completed=False,
        challenge=FlowChallenge(**result["challenge"]) if result.get("challenge") else None,
    )


@router.post("/flow/signup/start", response_model=FlowStartResponse)
async def flow_signup_start(
    executor: Annotated[FlowExecutorClient, Depends(get_flow_executor)],
) -> FlowStartResponse:
    """Start the enrollment (signup) flow."""
    try:
        flow_token, challenge = await executor.start_flow(
            authentik_settings.enrollment_flow_slug,
        )
        return FlowStartResponse(
            flow_token=flow_token,
            challenge=FlowChallenge(**challenge),
        )
    except FlowExecutorError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.post("/flow/signup/submit", response_model=FlowStepResponse)
async def flow_signup_submit(
    body: FlowSubmitRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    executor: Annotated[FlowExecutorClient, Depends(get_flow_executor)],
) -> FlowStepResponse:
    """Submit data to the signup flow."""
    try:
        result = await executor.submit_flow(
            body.flow_token,
            authentik_settings.enrollment_flow_slug,
            body.data,
        )
    except FlowExecutorError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e

    if result.get("error"):
        return FlowStepResponse(
            completed=False,
            error=result["error"],
            challenge=FlowChallenge(**result["challenge"]) if result.get("challenge") else None,
        )

    if result.get("completed"):
        return FlowStepResponse(completed=True)

    # Next challenge (e.g., email verification stage)
    return FlowStepResponse(
        completed=False,
        challenge=FlowChallenge(**result["challenge"]) if result.get("challenge") else None,
    )


@router.post("/flow/signup/resend-email")
async def flow_signup_resend_email(
    body: FlowSubmitRequest,
    executor: Annotated[FlowExecutorClient, Depends(get_flow_executor)],
) -> dict[str, str]:
    """Re-trigger the email verification stage by submitting empty data."""
    try:
        await executor.submit_flow(
            body.flow_token,
            authentik_settings.enrollment_flow_slug,
            body.data or {},
        )
        return {"message": "Verification email resent"}
    except FlowExecutorError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


# ── GitHub OAuth (direct, bypassing Authentik UI) ──────────────

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_API = "https://api.github.com/user"
GITHUB_EMAILS_API = "https://api.github.com/user/emails"


@router.get("/github/login")
async def github_login() -> RedirectResponse:
    """Redirect to GitHub OAuth authorization page."""
    if not authentik_settings.github_client_id:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="GitHub OAuth is not configured",
        )

    state = secrets.token_urlsafe(32)
    # Store state in Redis for CSRF validation (5 min TTL)
    r = await get_redis()
    await r.set(f"github_oauth_state:{state}", "1", ex=300)

    params = urlencode(
        {
            "client_id": authentik_settings.github_client_id,
            "redirect_uri": authentik_settings.github_redirect_uri,
            "scope": "user:email",
            "state": state,
        }
    )
    return RedirectResponse(
        url=f"{GITHUB_AUTHORIZE_URL}?{params}",
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/github/callback")
async def github_callback(
    db: Annotated[AsyncSession, Depends(get_db)],
    code: str | None = Query(None),
    state: str | None = Query(None),
    error: str | None = Query(None),
) -> RedirectResponse:
    """Handle GitHub OAuth callback: exchange code, get user, issue JWT."""
    if error:
        return RedirectResponse(url=f"/login?error={error}", status_code=status.HTTP_302_FOUND)

    if not code or not state:
        return RedirectResponse(
            url="/login?error=missing_params", status_code=status.HTTP_302_FOUND
        )

    # Validate CSRF state
    r = await get_redis()
    stored = await r.get(f"github_oauth_state:{state}")
    if not stored:
        return RedirectResponse(url="/login?error=invalid_state", status_code=status.HTTP_302_FOUND)
    await r.delete(f"github_oauth_state:{state}")

    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        token_resp = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": authentik_settings.github_client_id,
                "client_secret": authentik_settings.github_client_secret,
                "code": code,
                "redirect_uri": authentik_settings.github_redirect_uri,
            },
            headers={"Accept": "application/json"},
        )
        if token_resp.status_code != 200:
            logger.error("GitHub token exchange failed: %s", token_resp.text)
            return RedirectResponse(
                url="/login?error=token_exchange_failed", status_code=status.HTTP_302_FOUND
            )

        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            logger.error("No access_token in GitHub response: %s", token_data)
            return RedirectResponse(
                url="/login?error=no_access_token", status_code=status.HTTP_302_FOUND
            )

        auth_headers = {"Authorization": f"Bearer {access_token}"}

        # Get user profile
        user_resp = await client.get(GITHUB_USER_API, headers=auth_headers)
        if user_resp.status_code != 200:
            logger.error("GitHub user API failed: %s", user_resp.text)
            return RedirectResponse(
                url="/login?error=github_user_failed", status_code=status.HTTP_302_FOUND
            )
        gh_user = user_resp.json()

        # Get primary verified email
        email = gh_user.get("email")
        if not email:
            emails_resp = await client.get(GITHUB_EMAILS_API, headers=auth_headers)
            if emails_resp.status_code == 200:
                for em in emails_resp.json():
                    if em.get("primary") and em.get("verified"):
                        email = em["email"]
                        break

        if not email:
            return RedirectResponse(url="/login?error=no_email", status_code=status.HTTP_302_FOUND)

    # Find or create local user
    username = gh_user.get("login", email.split("@")[0])
    github_id = str(gh_user.get("id", ""))

    user = await _find_or_create_user(
        db,
        authentik_id=f"github:{github_id}",
        email=email,
        username=username,
    )

    # Issue JWT session cookie
    token = create_session_jwt(user)
    redirect = RedirectResponse(url="/?auth=github", status_code=status.HTTP_302_FOUND)
    _set_session_cookie(redirect, token)
    return redirect


# ── Session endpoints ───────────────────────────────────────────


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: CurrentActiveUser,
) -> UserResponse:
    """Get current authenticated user information."""
    return UserResponse.model_validate(current_user)


@router.post("/logout")
async def logout_post(
    response: Response,
    session_token: str | None = Cookie(
        None,
        alias=authentik_settings.session_cookie_name,
    ),
) -> dict[str, str]:
    """Logout: clear JWT session cookie."""
    _clear_session_cookie(response)
    return {"message": "Logged out successfully"}


@router.get("/logout")
async def logout_get(
    session_token: str | None = Cookie(
        None,
        alias=authentik_settings.session_cookie_name,
    ),
) -> RedirectResponse:
    """Logout via GET: clear cookie and redirect to login."""
    redirect = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    redirect.delete_cookie(
        key=authentik_settings.session_cookie_name,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return redirect
