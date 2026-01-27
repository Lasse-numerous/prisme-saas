"""Custom REST API routes for User.

✅ YOUR CODE - Safe to modify, will not be overwritten.
This file was generated once by Prism and is yours to customize.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from prisme_api.auth.dependencies import require_roles

from ._generated.user_routes import router as base_router

# Create a new router with admin-only access
# All user management endpoints require admin role
router = APIRouter(
    dependencies=[Depends(require_roles("admin"))],
)
router.include_router(base_router)


# Add your custom endpoints below
# Example:
# @router.get("/users/stats")
# async def get_user_stats(db: DbSession):
#     """Get statistics for users."""
#     pass


__all__ = ["router"]
