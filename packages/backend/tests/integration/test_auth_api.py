"""Integration tests for auth REST API endpoints."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pyotp
import pytest
import pytest_asyncio

from prisme_api.auth.utils import generate_token, generate_totp_secret, hash_password
from prisme_api.models.user import User

# ── Helpers ──────────────────────────────────────────────────────


async def _create_verified_user(db, email="user@example.com", password="StrongPass1") -> User:
    """Create a verified, active user in the database."""
    user = User(
        email=email,
        username=email.split("@")[0],
        password_hash=hash_password(password),
        email_verified=True,
        is_active=True,
        roles=["user"],
        failed_login_attempts=0,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def _create_unverified_user(
    db, email="unverified@example.com", password="StrongPass1", *, expired: bool = False
) -> User:
    token = generate_token()
    user = User(
        email=email,
        username=email.split("@")[0],
        password_hash=hash_password(password),
        email_verified=False,
        email_verification_token=token,
        # Don't set expiry by default (SQLite strips timezone info).
        # For expired-token tests, set it in the past as naive datetime.
        email_verification_token_expires_at=None,
        is_active=True,
        roles=["user"],
        failed_login_attempts=0,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# ── Signup ───────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestSignup:
    @patch("prisme_api.api.rest.auth._validate_email_domain", return_value=None)
    @patch("prisme_api.api.rest.auth.send_verification_email")
    async def test_signup_success(self, mock_email, mock_domain, unauthenticated_client, db):
        resp = await unauthenticated_client.post(
            "/api/auth/signup",
            json={"email": "new@example.com", "username": "newuser", "password": "StrongPass1"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data
        mock_email.assert_called_once()

    @patch("prisme_api.api.rest.auth._validate_email_domain", return_value=None)
    @patch("prisme_api.api.rest.auth.send_verification_email")
    async def test_signup_duplicate_email(
        self, mock_email, mock_domain, unauthenticated_client, db
    ):
        await _create_verified_user(db, email="dup@example.com")
        resp = await unauthenticated_client.post(
            "/api/auth/signup",
            json={"email": "dup@example.com", "username": "dup", "password": "StrongPass1"},
        )
        assert resp.status_code == 409

    async def test_signup_weak_password(self, unauthenticated_client, db):
        resp = await unauthenticated_client.post(
            "/api/auth/signup",
            json={"email": "weak@example.com", "username": "weak", "password": "short"},
        )
        assert resp.status_code == 400


# ── Email Verification ───────────────────────────────────────────


@pytest.mark.asyncio
class TestEmailVerification:
    async def test_verify_email_success(self, unauthenticated_client, db):
        user = await _create_unverified_user(db, email="verify@example.com")
        token = user.email_verification_token
        resp = await unauthenticated_client.post("/api/auth/verify-email", json={"token": token})
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "Email verified"
        assert "user" in data

    async def test_verify_email_invalid_token(self, unauthenticated_client, db):
        resp = await unauthenticated_client.post(
            "/api/auth/verify-email", json={"token": "bad-token"}
        )
        assert resp.status_code == 400

    async def test_verify_email_expired_token(self, unauthenticated_client, db):
        user = await _create_unverified_user(db, email="expired@example.com")
        user.email_verification_token_expires_at = datetime.now(UTC) - timedelta(hours=1)
        await db.commit()

        resp = await unauthenticated_client.post(
            "/api/auth/verify-email",
            json={"token": user.email_verification_token},
        )
        assert resp.status_code == 400

    @patch("prisme_api.api.rest.auth.send_verification_email")
    async def test_resend_verification(self, mock_email, unauthenticated_client, db):
        await _create_unverified_user(db, email="resend@example.com")
        resp = await unauthenticated_client.post(
            "/api/auth/resend-verification", json={"email": "resend@example.com"}
        )
        assert resp.status_code == 200
        # Always 200 even for nonexistent
        resp2 = await unauthenticated_client.post(
            "/api/auth/resend-verification", json={"email": "nobody@example.com"}
        )
        assert resp2.status_code == 200


# ── Login ────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestLogin:
    async def test_login_success(self, unauthenticated_client, db):
        await _create_verified_user(db, email="login@example.com", password="StrongPass1")
        resp = await unauthenticated_client.post(
            "/api/auth/login",
            json={"email": "login@example.com", "password": "StrongPass1"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["requires_mfa"] is False
        assert data["user"] is not None
        assert "prisme_api_session" in resp.cookies

    async def test_login_wrong_password(self, unauthenticated_client, db):
        await _create_verified_user(db, email="wrongpw@example.com")
        resp = await unauthenticated_client.post(
            "/api/auth/login",
            json={"email": "wrongpw@example.com", "password": "WrongPassword1"},
        )
        assert resp.status_code == 401

    async def test_login_unverified_email(self, unauthenticated_client, db):
        await _create_unverified_user(db, email="unver_login@example.com", password="StrongPass1")
        resp = await unauthenticated_client.post(
            "/api/auth/login",
            json={"email": "unver_login@example.com", "password": "StrongPass1"},
        )
        assert resp.status_code == 403

    async def test_login_inactive_user(self, unauthenticated_client, db):
        user = await _create_verified_user(db, email="inactive@example.com")
        user.is_active = False
        await db.commit()
        resp = await unauthenticated_client.post(
            "/api/auth/login",
            json={"email": "inactive@example.com", "password": "StrongPass1"},
        )
        assert resp.status_code == 403

    @pytest.mark.xfail(
        reason="SQLite strips timezone info causing naive/aware datetime comparison error"
    )
    async def test_login_account_lockout(self, unauthenticated_client, db):
        await _create_verified_user(db, email="locked@example.com")
        for _ in range(5):
            await unauthenticated_client.post(
                "/api/auth/login",
                json={"email": "locked@example.com", "password": "WrongPassword1"},
            )
        resp = await unauthenticated_client.post(
            "/api/auth/login",
            json={"email": "locked@example.com", "password": "StrongPass1"},
        )
        assert resp.status_code == 423

    async def test_login_lockout_expires(self, unauthenticated_client, db):
        user = await _create_verified_user(db, email="lockexp@example.com")
        user.failed_login_attempts = 5
        user.locked_until = datetime.now(UTC) - timedelta(minutes=1)
        await db.commit()
        resp = await unauthenticated_client.post(
            "/api/auth/login",
            json={"email": "lockexp@example.com", "password": "StrongPass1"},
        )
        assert resp.status_code == 200

    async def test_login_mfa_required(self, unauthenticated_client, db):
        user = await _create_verified_user(db, email="mfauser@example.com")
        user.mfa_enabled = True
        user.mfa_secret = generate_totp_secret()
        await db.commit()
        resp = await unauthenticated_client.post(
            "/api/auth/login",
            json={"email": "mfauser@example.com", "password": "StrongPass1"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["requires_mfa"] is True
        assert data["user"] is None
        assert "prisme_api_session" not in resp.cookies


# ── MFA Login ────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestMFALogin:
    async def test_login_mfa_success(self, unauthenticated_client, db):
        secret = generate_totp_secret()
        user = await _create_verified_user(db, email="mfalogin@example.com")
        user.mfa_enabled = True
        user.mfa_secret = secret
        await db.commit()

        code = pyotp.TOTP(secret).now()
        resp = await unauthenticated_client.post(
            "/api/auth/login/mfa",
            json={"email": "mfalogin@example.com", "code": code},
        )
        assert resp.status_code == 200
        assert "prisme_api_session" in resp.cookies

    async def test_login_mfa_invalid_code(self, unauthenticated_client, db):
        secret = generate_totp_secret()
        user = await _create_verified_user(db, email="mfabad@example.com")
        user.mfa_enabled = True
        user.mfa_secret = secret
        await db.commit()

        resp = await unauthenticated_client.post(
            "/api/auth/login/mfa",
            json={"email": "mfabad@example.com", "code": "000000"},
        )
        assert resp.status_code == 401


# ── Password Reset ───────────────────────────────────────────────


@pytest.mark.asyncio
class TestPasswordReset:
    @patch("prisme_api.api.rest.auth.send_password_reset_email")
    async def test_forgot_password(self, mock_email, unauthenticated_client, db):
        await _create_verified_user(db, email="forgot@example.com")
        resp = await unauthenticated_client.post(
            "/api/auth/forgot-password", json={"email": "forgot@example.com"}
        )
        assert resp.status_code == 200
        # Always 200 for non-existent too
        resp2 = await unauthenticated_client.post(
            "/api/auth/forgot-password", json={"email": "nobody@example.com"}
        )
        assert resp2.status_code == 200

    @patch("prisme_api.api.rest.auth.send_password_changed_notification")
    async def test_reset_password_success(self, mock_email, unauthenticated_client, db):
        user = await _create_verified_user(db, email="reset@example.com")
        token = generate_token()
        user.password_reset_token = token
        user.password_reset_token_expires_at = datetime.now(UTC) + timedelta(hours=1)
        await db.commit()

        resp = await unauthenticated_client.post(
            "/api/auth/reset-password",
            json={"token": token, "password": "NewStrong1"},
        )
        assert resp.status_code == 200
        assert "prisme_api_session" in resp.cookies

    async def test_reset_password_invalid_token(self, unauthenticated_client, db):
        resp = await unauthenticated_client.post(
            "/api/auth/reset-password",
            json={"token": "bad-token", "password": "NewStrong1"},
        )
        assert resp.status_code == 400

    @patch("prisme_api.api.rest.auth.send_password_changed_notification")
    async def test_reset_password_expired_token(self, mock_email, unauthenticated_client, db):
        user = await _create_verified_user(db, email="resetexp@example.com")
        token = generate_token()
        user.password_reset_token = token
        user.password_reset_token_expires_at = datetime.now(UTC) - timedelta(hours=1)
        await db.commit()

        resp = await unauthenticated_client.post(
            "/api/auth/reset-password",
            json={"token": token, "password": "NewStrong1"},
        )
        assert resp.status_code == 400

    async def test_reset_password_weak_password(self, unauthenticated_client, db):
        user = await _create_verified_user(db, email="resetweak@example.com")
        token = generate_token()
        user.password_reset_token = token
        user.password_reset_token_expires_at = datetime.now(UTC) + timedelta(hours=1)
        await db.commit()

        resp = await unauthenticated_client.post(
            "/api/auth/reset-password",
            json={"token": token, "password": "weak"},
        )
        assert resp.status_code == 400


# ── MFA Setup (authenticated) ───────────────────────────────────


@pytest_asyncio.fixture
async def authenticated_client(db):
    """Client with a real persisted user for MFA tests."""
    from httpx import ASGITransport, AsyncClient

    from prisme_api.auth.dependencies import get_current_active_user
    from prisme_api.database import get_db
    from prisme_api.main import app

    unique = uuid.uuid4().hex[:8]
    user = User(
        email=f"authuser-{unique}@example.com",
        username=f"authuser-{unique}",
        password_hash=hash_password("StrongPass1"),
        email_verified=True,
        is_active=True,
        roles=["admin"],
        failed_login_attempts=0,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    async def override_get_db():
        yield db

    async def override_get_current_active_user():
        # Re-fetch to get latest state
        await db.refresh(user)
        return user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.mark.asyncio
class TestMFASetup:
    async def test_mfa_setup(self, authenticated_client, db):
        resp = await authenticated_client.post("/api/auth/mfa/setup")
        assert resp.status_code == 200
        data = resp.json()
        assert "totp_uri" in data
        assert "secret" in data
        assert data["totp_uri"].startswith("otpauth://")

    async def test_mfa_verify_setup(self, authenticated_client, db):
        setup_resp = await authenticated_client.post("/api/auth/mfa/setup")
        secret = setup_resp.json()["secret"]

        code = pyotp.TOTP(secret).now()
        resp = await authenticated_client.post("/api/auth/mfa/verify-setup", json={"code": code})
        assert resp.status_code == 200

    async def test_mfa_verify_setup_invalid_code(self, authenticated_client, db):
        await authenticated_client.post("/api/auth/mfa/setup")
        resp = await authenticated_client.post(
            "/api/auth/mfa/verify-setup", json={"code": "000000"}
        )
        assert resp.status_code == 400

    async def test_mfa_disable(self, authenticated_client, db):
        resp = await authenticated_client.post(
            "/api/auth/mfa/disable", json={"password": "StrongPass1"}
        )
        assert resp.status_code == 200

    async def test_mfa_disable_wrong_password(self, authenticated_client, db):
        resp = await authenticated_client.post("/api/auth/mfa/disable", json={"password": "wrong"})
        assert resp.status_code == 401


# ── Session ──────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestSession:
    async def test_auth_me(self, authenticated_client, db):
        resp = await authenticated_client.get("/api/auth/me")
        assert resp.status_code == 200
        data = resp.json()
        assert "email" in data
        assert "roles" in data

    async def test_auth_me_unauthenticated(self, unauthenticated_client, db):
        resp = await unauthenticated_client.get("/api/auth/me")
        assert resp.status_code == 401

    async def test_logout(self, unauthenticated_client, db):
        resp = await unauthenticated_client.post("/api/auth/logout")
        assert resp.status_code == 200
        assert resp.json()["message"] == "Logged out successfully"
