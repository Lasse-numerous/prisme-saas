"""Service for Subdomain.

Custom service logic for managing subdomains with Hetzner DNS integration.
"""

from __future__ import annotations

from sqlalchemy import select

from prisme_api.models.subdomain import Subdomain

from ._generated.subdomain_base import SubdomainServiceBase


class SubdomainService(SubdomainServiceBase):
    """Custom service logic for Subdomain.

    Extends the base service with:
    - Lookup by name (unique field)
    - Subdomain validation
    """

    async def get_by_name(self, name: str) -> Subdomain | None:
        """Get a subdomain by its unique name.

        Args:
            name: The subdomain name (e.g., 'myapp')

        Returns:
            The Subdomain object if found, None otherwise
        """
        query = select(self.model).where(self.model.name == name.lower())
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


__all__ = ["SubdomainService"]
