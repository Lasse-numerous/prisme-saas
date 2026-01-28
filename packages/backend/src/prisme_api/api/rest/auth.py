"""Authentication routes using Authentik Flow Executor API.

Custom auth UX: the frontend drives Authentik flows through these endpoints.
"""

from __future__ import annotations

import logging
import os
from typing import Annotated

import redis.asyncio as redis
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
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


# ── GitHub OAuth (via Authentik source) ─────────────────────────


@router.get("/github/login")
async def github_login() -> RedirectResponse:
    """Redirect to Authentik GitHub OAuth source."""
    base = authentik_settings.authentik_base_url.rstrip("/")
    url = f"{base}/source/oauth/login/github/"
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.get("/github/callback")
async def github_callback(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    code: str | None = None,
    error: str | None = None,
) -> RedirectResponse:
    """Handle GitHub OAuth callback from Authentik.

    After Authentik processes the GitHub OAuth, it redirects here.
    We find/create the local user and set a JWT cookie.
    """
    if error:
        return RedirectResponse(url=f"/login?error={error}", status_code=status.HTTP_302_FOUND)

    # Authentik handles the GitHub OAuth token exchange and creates/links the user.
    # The callback arrives with Authentik session cookies set.
    # We need to get user info from Authentik's userinfo endpoint.
    # For now, redirect to the app — the frontend will call /auth/me.
    redirect = RedirectResponse(url="/?auth=github", status_code=status.HTTP_302_FOUND)
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
