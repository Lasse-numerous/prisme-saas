"""Service for AllowedEmailDomain.

Manages email domain whitelist for user signups.
"""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from prisme_api.models.allowed_email_domain import AllowedEmailDomain

from ._generated.allowed_email_domain_base import AllowedEmailDomainServiceBase

logger = logging.getLogger(__name__)


class AllowedEmailDomainService(AllowedEmailDomainServiceBase):
    """Service for managing allowed email domains.

    Extends the base service with domain validation methods.
    """

    model = AllowedEmailDomain

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the service with a database session.

        Args:
            db: The async database session.
        """
        super().__init__(db)

    async def get_by_domain(self, domain: str) -> AllowedEmailDomain | None:
        """Get an allowed domain by its domain name.

        Args:
            domain: The email domain (e.g., 'example.com')

        Returns:
            The AllowedEmailDomain object if found, None otherwise
        """
        query = select(self.model).where(self.model.domain == domain.lower())
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def is_domain_allowed(self, email: str) -> bool:
        """Check if an email address is from an allowed domain.

        Args:
            email: Full email address (e.g., 'user@example.com')

        Returns:
            True if the email domain is in the whitelist and active
        """
        if "@" not in email:
            return False

        domain = email.split("@")[1].lower()
        allowed = await self.get_by_domain(domain)

        if allowed and allowed.is_active:
            return True

        # Also check if whitelist is empty (allow all in that case)
        count = await self.count()
        if count == 0:
            logger.warning("Email domain whitelist is empty - allowing all domains")
            return True

        return False

    async def list_active_domains(self) -> list[str]:
        """Get list of all active allowed domains.

        Returns:
            List of domain strings
        """
        query = select(self.model.domain).where(self.model.is_active == True)  # noqa: E712
        result = await self.db.execute(query)
        return list(result.scalars().all())


__all__ = ["AllowedEmailDomainService"]
