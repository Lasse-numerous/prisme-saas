"""Authentication utility functions.

Password hashing, token generation, TOTP support.
"""

from __future__ import annotations

import re
import secrets

import bcrypt
import pyotp


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def validate_password_strength(password: str) -> str | None:
    """Validate password strength. Returns error message or None if valid."""
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return "Password must contain at least one digit"
    return None


def generate_token() -> str:
    """Generate a cryptographically secure URL-safe token."""
    return secrets.token_urlsafe(32)


def generate_totp_secret() -> str:
    """Generate a TOTP secret key."""
    return pyotp.random_base32()


def get_totp_uri(secret: str, email: str, issuer: str = "MadeWithPris.me") -> str:
    """Get the otpauth:// URI for QR code generation."""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=issuer)


def verify_totp(secret: str, code: str) -> bool:
    """Verify a TOTP code against a secret."""
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)
