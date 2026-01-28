"""SQLAlchemy model for AllowedEmailDomain.

Whitelisted email domains for user signup.
"""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class AllowedEmailDomain(Base, TimestampMixin):
    """Whitelisted email domains for user signup"""

    __tablename__ = "allowed_email_domains"

    id: Mapped[int] = mapped_column(primary_key=True)
    domain: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
