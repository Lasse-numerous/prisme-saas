"""Unit tests for auth/utils.py."""

from __future__ import annotations

import pyotp

from prisme_api.auth.utils import (
    generate_token,
    generate_totp_secret,
    get_totp_uri,
    hash_password,
    validate_password_strength,
    verify_password,
    verify_totp,
)


class TestPasswordHashing:
    def test_hash_and_verify_password(self):
        hashed = hash_password("SecurePass1")
        assert verify_password("SecurePass1", hashed)

    def test_verify_password_wrong(self):
        hashed = hash_password("SecurePass1")
        assert not verify_password("WrongPassword1", hashed)

    def test_hash_is_different_each_time(self):
        h1 = hash_password("SecurePass1")
        h2 = hash_password("SecurePass1")
        assert h1 != h2  # bcrypt uses random salt


class TestPasswordStrength:
    def test_too_short(self):
        assert validate_password_strength("Ab1") is not None
        assert "8 characters" in validate_password_strength("Ab1")

    def test_no_uppercase(self):
        result = validate_password_strength("abcdefg1")
        assert result is not None
        assert "uppercase" in result

    def test_no_lowercase(self):
        result = validate_password_strength("ABCDEFG1")
        assert result is not None
        assert "lowercase" in result

    def test_no_digit(self):
        result = validate_password_strength("Abcdefgh")
        assert result is not None
        assert "digit" in result

    def test_valid(self):
        assert validate_password_strength("Abcdefg1") is None


class TestTokenGeneration:
    def test_generate_token(self):
        token = generate_token()
        assert isinstance(token, str)
        assert len(token) > 20  # 32 bytes base64 → ~43 chars

    def test_tokens_are_unique(self):
        assert generate_token() != generate_token()


class TestTOTP:
    def test_generate_totp_secret(self):
        secret = generate_totp_secret()
        assert isinstance(secret, str)
        assert len(secret) >= 16  # base32 encoded

    def test_get_totp_uri(self):
        secret = generate_totp_secret()
        uri = get_totp_uri(secret, "user@example.com")
        assert uri.startswith("otpauth://totp/")
        assert "user" in uri and "example.com" in uri
        assert "MadeWithPris.me" in uri

    def test_verify_totp_valid(self):
        secret = generate_totp_secret()
        totp = pyotp.TOTP(secret)
        code = totp.now()
        assert verify_totp(secret, code) is True

    def test_verify_totp_invalid(self):
        secret = generate_totp_secret()
        assert verify_totp(secret, "000000") is False
