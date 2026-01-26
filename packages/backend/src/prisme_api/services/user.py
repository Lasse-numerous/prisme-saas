"""Service for User.

✅ YOUR CODE - Safe to modify, will not be overwritten.
This file was generated once by Prism and is yours to customize.
"""

from __future__ import annotations

from ._generated.user_base import UserServiceBase


class UserService(UserServiceBase):
    """Custom service logic for User.

    Add your custom methods and override base methods here.
    """

    # Example: Override a lifecycle hook
    # async def before_create(self, data: UserCreate) -> None:
    #     # Custom validation or transformation
    #     pass

    # Example: Add a custom method
    # async def find_by_email(self, email: str) -> User | None:
    #     query = select(self.model).where(self.model.email == email)
    #     result = await self.db.execute(query)
    #     return result.scalar_one_or_none()

    pass


__all__ = ["UserService"]
