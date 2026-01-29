"""Authentication routes — self-contained (no Authentik).

Signup, login, email verification, password reset, MFA/TOTP, GitHub OAuth.
"""

from __future__ import annotations

import logging
import os
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Cookie, Depends, HTTPException, Query, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from prisme_api.auth.config import auth_settings
from prisme_api.auth.dependencies import CurrentActiveUser, create_session_jwt
from prisme_api.auth.utils import (
    generate_token,
    generate_totp_secret,
    get_totp_uri,
    hash_password,
    validate_password_strength,
    verify_password,
    verify_totp,
)
from prisme_api.database import get_db
from prisme_api.models.user import User
from prisme_api.schemas.auth import UserResponse
from prisme_api.services.email_service import (
    send_password_changed_notification,
    send_password_reset_email,
    send_verification_email,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


# ── Request/Response schemas ────────────────────────────────────


class SignupRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginMFARequest(BaseModel):
    email: EmailStr
    code: str


class VerifyEmailRequest(BaseModel):
    token: str


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    password: str


class MFAVerifySetupRequest(BaseModel):
    code: str


class MFADisableRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    requires_mfa: bool = False
    user: dict | None = None


class MFASetupResponse(BaseModel):
    totp_uri: str
    secret: str


# ── Helpers ─────────────────────────────────────────────────────


def _is_secure_context() -> bool:
    debug = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    return not debug


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=auth_settings.session_cookie_name,
        value=token,
        max_age=auth_settings.session_max_age,
        httponly=True,
        secure=_is_secure_context(),
        samesite="lax",
    )


def _clear_session_cookie(response: Response) -> None:
    response.delete_cookie(
        key=auth_settings.session_cookie_name,
        httponly=True,
        secure=_is_secure_context(),
        samesite="lax",
    )


def _check_account_locked(user: User) -> None:
    """Raise 423 if the account is currently locked."""
    if user.locked_until and user.locked_until > datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account temporarily locked due to too many failed login attempts. Try again later.",
        )


def _record_failed_login(user: User) -> None:
    """Increment failed attempts and lock if threshold reached."""
    user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
    if user.failed_login_attempts >= auth_settings.max_failed_login_attempts:
        user.locked_until = datetime.now(UTC) + timedelta(
            minutes=auth_settings.lockout_duration_minutes
        )


def _reset_failed_logins(user: User) -> None:
    user.failed_login_attempts = 0
    user.locked_until = None


async def _validate_email_domain(db: AsyncSession, email: str) -> None:
    """Check email domain against whitelist."""
    try:
        from prisme_api.services.allowed_email_domain import AllowedEmailDomainService

        domain_service = AllowedEmailDomainService(db)
        if not await domain_service.is_domain_allowed(email):
            domain = email.split("@")[1] if "@" in email else "unknown"
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Email domain '{domain}' is not allowed for signup.",
            )
    except ImportError:
        pass


# ── Signup ──────────────────────────────────────────────────────


@router.post("/signup")
async def signup(
    body: SignupRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    """Create a new user account and send verification email."""
    # Validate password
    pw_error = validate_password_strength(body.password)
    if pw_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=pw_error)

    # Check if email already exists
    result = await db.execute(select(User).where(User.email == body.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    # Validate email domain
    await _validate_email_domain(db, body.email)

    # Create user
    token = generate_token()
    user = User(
        email=body.email,
        username=body.username,
        password_hash=hash_password(body.password),
        email_verified=False,
        email_verification_token=token,
        email_verification_token_expires_at=datetime.now(UTC)
        + timedelta(hours=auth_settings.email_verification_token_hours),
        roles=["user"],
        is_active=True,
    )
    db.add(user)
    await db.commit()

    # Send verification email
    send_verification_email(body.email, token)

    return {"message": "Account created. Please check your email to verify your address."}


# ── Email verification ──────────────────────────────────────────


@router.post("/verify-email")
async def verify_email(
    body: VerifyEmailRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Verify email address and auto-login."""
    result = await db.execute(select(User).where(User.email_verification_token == body.token))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token.",
        )

    if (
        user.email_verification_token_expires_at
        and user.email_verification_token_expires_at < datetime.now(UTC)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired. Please request a new one.",
        )

    user.email_verified = True
    user.email_verification_token = None
    user.email_verification_token_expires_at = None
    await db.commit()
    await db.refresh(user)

    # Auto-login
    token = create_session_jwt(user)
    _set_session_cookie(response, token)

    return {"message": "Email verified", "user": UserResponse.model_validate(user).model_dump()}


@router.post("/resend-verification")
async def resend_verification(
    body: ResendVerificationRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    """Resend verification email. Always returns 200 to prevent email enumeration."""
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if user and not user.email_verified:
        token = generate_token()
        user.email_verification_token = token
        user.email_verification_token_expires_at = datetime.now(UTC) + timedelta(
            hours=auth_settings.email_verification_token_hours
        )
        await db.commit()
        send_verification_email(body.email, token)

    return {"message": "If an unverified account exists, a verification email has been sent."}


# ── Login ───────────────────────────────────────────────────────


@router.post("/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LoginResponse:
    """Login with email and password. Returns requires_mfa if MFA is enabled."""
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    _check_account_locked(user)

    if not verify_password(body.password, user.password_hash):
        _record_failed_login(user)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    _reset_failed_logins(user)

    if not user.email_verified:
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in.",
        )

    if not user.is_active:
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive.",
        )

    if user.mfa_enabled and user.mfa_secret:
        await db.commit()
        return LoginResponse(requires_mfa=True)

    await db.commit()

    token = create_session_jwt(user)
    _set_session_cookie(response, token)
    return LoginResponse(
        requires_mfa=False,
        user=UserResponse.model_validate(user).model_dump(),
    )


@router.post("/login/mfa", response_model=LoginResponse)
async def login_mfa(
    body: LoginMFARequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LoginResponse:
    """Complete MFA login with TOTP code."""
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if not user or not user.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    _check_account_locked(user)

    if not verify_totp(user.mfa_secret, body.code):
        _record_failed_login(user)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid TOTP code.",
        )

    _reset_failed_logins(user)
    await db.commit()

    token = create_session_jwt(user)
    _set_session_cookie(response, token)
    return LoginResponse(
        requires_mfa=False,
        user=UserResponse.model_validate(user).model_dump(),
    )


# ── Password reset ──────────────────────────────────────────────


@router.post("/forgot-password")
async def forgot_password(
    body: ForgotPasswordRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    """Send password reset email. Always returns 200 to prevent email enumeration."""
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if user:
        token = generate_token()
        user.password_reset_token = token
        user.password_reset_token_expires_at = datetime.now(UTC) + timedelta(
            hours=auth_settings.password_reset_token_hours
        )
        await db.commit()
        send_password_reset_email(body.email, token)

    return {"message": "If an account exists, a password reset email has been sent."}


@router.post("/reset-password")
async def reset_password(
    body: ResetPasswordRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Reset password using token and auto-login."""
    pw_error = validate_password_strength(body.password)
    if pw_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=pw_error)

    result = await db.execute(select(User).where(User.password_reset_token == body.token))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token.",
        )

    if user.password_reset_token_expires_at and user.password_reset_token_expires_at < datetime.now(
        UTC
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired.",
        )

    user.password_hash = hash_password(body.password)
    user.password_reset_token = None
    user.password_reset_token_expires_at = None
    _reset_failed_logins(user)
    await db.commit()
    await db.refresh(user)

    send_password_changed_notification(user.email)

    # Auto-login
    token = create_session_jwt(user)
    _set_session_cookie(response, token)

    return {"message": "Password reset", "user": UserResponse.model_validate(user).model_dump()}


# ── MFA / TOTP ──────────────────────────────────────────────────


@router.post("/mfa/setup", response_model=MFASetupResponse)
async def mfa_setup(
    current_user: CurrentActiveUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MFASetupResponse:
    """Generate TOTP secret and URI for QR code. Requires authentication."""
    secret = generate_totp_secret()
    # Store pending secret (not yet enabled)
    current_user.mfa_secret = secret
    await db.commit()

    uri = get_totp_uri(secret, current_user.email)
    return MFASetupResponse(totp_uri=uri, secret=secret)


@router.post("/mfa/verify-setup")
async def mfa_verify_setup(
    body: MFAVerifySetupRequest,
    current_user: CurrentActiveUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    """Verify TOTP code and enable MFA."""
    if not current_user.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA setup not started. Call /auth/mfa/setup first.",
        )

    if not verify_totp(current_user.mfa_secret, body.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid TOTP code.",
        )

    current_user.mfa_enabled = True
    await db.commit()
    return {"message": "MFA enabled successfully."}


@router.post("/mfa/disable")
async def mfa_disable(
    body: MFADisableRequest,
    current_user: CurrentActiveUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    """Disable MFA. Requires password verification."""
    if not current_user.password_hash or not verify_password(
        body.password, current_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password.",
        )

    current_user.mfa_enabled = False
    current_user.mfa_secret = None
    await db.commit()
    return {"message": "MFA disabled."}


# ── GitHub OAuth ────────────────────────────────────────────────

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_API = "https://api.github.com/user"
GITHUB_EMAILS_API = "https://api.github.com/user/emails"

# In-memory state store (acceptable for single-instance; use Redis if scaling)
_oauth_states: dict[str, float] = {}


def _cleanup_expired_states() -> None:
    now = datetime.now(UTC).timestamp()
    expired = [k for k, v in _oauth_states.items() if now - v > 300]
    for k in expired:
        _oauth_states.pop(k, None)


@router.get("/github/login")
async def github_login() -> RedirectResponse:
    """Redirect to GitHub OAuth authorization page."""
    if not auth_settings.github_client_id:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="GitHub OAuth is not configured",
        )

    _cleanup_expired_states()
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = datetime.now(UTC).timestamp()

    params = urlencode(
        {
            "client_id": auth_settings.github_client_id,
            "redirect_uri": auth_settings.github_redirect_uri,
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
    """Handle GitHub OAuth callback."""
    if error:
        return RedirectResponse(url=f"/login?error={error}", status_code=status.HTTP_302_FOUND)

    if not code or not state:
        return RedirectResponse(
            url="/auth/callback?error=missing_params", status_code=status.HTTP_302_FOUND
        )

    # Validate CSRF state
    if state not in _oauth_states:
        return RedirectResponse(
            url="/auth/callback?error=invalid_state", status_code=status.HTTP_302_FOUND
        )
    _oauth_states.pop(state, None)

    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        token_resp = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": auth_settings.github_client_id,
                "client_secret": auth_settings.github_client_secret,
                "code": code,
                "redirect_uri": auth_settings.github_redirect_uri,
            },
            headers={"Accept": "application/json"},
        )
        if token_resp.status_code != 200:
            logger.error("GitHub token exchange failed: %s", token_resp.text)
            return RedirectResponse(
                url="/auth/callback?error=token_exchange_failed",
                status_code=status.HTTP_302_FOUND,
            )

        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return RedirectResponse(
                url="/auth/callback?error=no_access_token",
                status_code=status.HTTP_302_FOUND,
            )

        auth_headers = {"Authorization": f"Bearer {access_token}"}

        # Get user profile
        user_resp = await client.get(GITHUB_USER_API, headers=auth_headers)
        if user_resp.status_code != 200:
            return RedirectResponse(
                url="/auth/callback?error=github_user_failed",
                status_code=status.HTTP_302_FOUND,
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
            return RedirectResponse(
                url="/auth/callback?error=no_email", status_code=status.HTTP_302_FOUND
            )

    # Find or create user
    username = gh_user.get("login", email.split("@")[0])
    github_id = str(gh_user.get("id", ""))

    # Try finding by github_id first
    result = await db.execute(select(User).where(User.github_id == github_id))
    user = result.scalar_one_or_none()

    if not user:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

    if user:
        # Link github_id if not set
        if not user.github_id:
            user.github_id = github_id
            await db.commit()
    else:
        # Validate email domain
        await _validate_email_domain(db, email)

        user = User(
            email=email,
            username=username,
            github_id=github_id,
            email_verified=True,  # GitHub emails are verified
            is_active=True,
            roles=["user"],
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token = create_session_jwt(user)
    redirect = RedirectResponse(url="/auth/callback", status_code=status.HTTP_302_FOUND)
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
    session_token: str | None = Cookie(None, alias=auth_settings.session_cookie_name),
) -> dict[str, str]:
    """Logout: clear JWT session cookie."""
    _clear_session_cookie(response)
    return {"message": "Logged out successfully"}


@router.get("/logout")
async def logout_get(
    session_token: str | None = Cookie(None, alias=auth_settings.session_cookie_name),
) -> RedirectResponse:
    """Logout via GET: clear cookie and redirect to login."""
    redirect = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    redirect.delete_cookie(
        key=auth_settings.session_cookie_name,
        httponly=True,
        secure=_is_secure_context(),
        samesite="lax",
    )
    return redirect
