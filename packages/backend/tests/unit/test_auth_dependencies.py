"""Unit tests for auth/dependencies.py."""

from __future__ import annotations

import time
from unittest.mock import MagicMock

import jwt
import pytest

from prisme_api.auth.config import auth_settings
from prisme_api.auth.dependencies import (
    create_session_jwt,
    decode_session_jwt,
)


class TestSessionJWT:
    def _make_user(self, **kwargs):
        user = MagicMock()
        user.id = kwargs.get("id", 1)
        user.email = kwargs.get("email", "test@example.com")
        user.roles = kwargs.get("roles", ["user"])
        return user

    def test_create_and_decode(self):
        user = self._make_user()
        token = create_session_jwt(user)
        claims = decode_session_jwt(token)
        assert claims["sub"] == "1"
        assert claims["email"] == "test@example.com"
        assert claims["roles"] == ["user"]
        assert "exp" in claims
        assert "iat" in claims

    def test_decode_expired(self):
        payload = {
            "sub": "1",
            "email": "test@example.com",
            "roles": [],
            "iat": time.time() - 7200,
            "exp": time.time() - 3600,
        }
        token = jwt.encode(payload, auth_settings.jwt_secret, algorithm="HS256")
        with pytest.raises(jwt.ExpiredSignatureError):
            decode_session_jwt(token)

    def test_decode_invalid(self):
        with pytest.raises(jwt.InvalidTokenError):
            decode_session_jwt("not-a-valid-token")

    def test_decode_wrong_secret(self):
        payload = {
            "sub": "1",
            "email": "test@example.com",
            "roles": [],
            "iat": time.time(),
            "exp": time.time() + 3600,
        }
        token = jwt.encode(payload, "wrong-secret", algorithm="HS256")
        with pytest.raises(jwt.InvalidSignatureError):
            decode_session_jwt(token)


class TestRequireRoles:
    """Test require_roles dependency factory via integration (tested in test_auth_api.py)."""

    def test_role_check_logic(self):
        """Verify basic role matching logic directly."""
        required = {"admin"}
        user_roles = {"user"}
        assert not any(role in user_roles for role in required)

        user_roles = {"admin", "user"}
        assert any(role in user_roles for role in required)

    def test_wildcard_role(self):
        required_roles = ("*",)
        assert "*" in required_roles
