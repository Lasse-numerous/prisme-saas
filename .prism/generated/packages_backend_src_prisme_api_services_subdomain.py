"""Service for Subdomain.

✅ YOUR CODE - Safe to modify, will not be overwritten.
This file was generated once by Prism and is yours to customize.
"""

from __future__ import annotations

from ._generated.subdomain_base import SubdomainServiceBase


class SubdomainService(SubdomainServiceBase):
    """Custom service logic for Subdomain.

    Add your custom methods and override base methods here.
    """

    # Example: Override a lifecycle hook
    # async def before_create(self, data: SubdomainCreate) -> None:
    #     # Custom validation or transformation
    #     pass

    # Example: Add a custom method
    # async def find_by_email(self, email: str) -> Subdomain | None:
    #     query = select(self.model).where(self.model.email == email)
    #     result = await self.db.execute(query)
    #     return result.scalar_one_or_none()

    pass


__all__ = ["SubdomainService"]
