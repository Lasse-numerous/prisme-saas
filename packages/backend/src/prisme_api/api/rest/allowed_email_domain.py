"""Custom REST API routes for AllowedEmailDomain.

✅ YOUR CODE - Safe to modify, will not be overwritten.
This file was generated once by Prism and is yours to customize.
"""

from __future__ import annotations

from fastapi import APIRouter

from ._generated.allowed_email_domain_routes import router as base_router

# Create a new router that includes the base routes
router = APIRouter()
router.include_router(base_router)


# Add your custom endpoints below
# Example:
# @router.get("/allowed_email_domains/stats")
# async def get_allowed_email_domain_stats(db: DbSession):
#     """Get statistics for allowed_email_domains."""
#     pass


__all__ = ["router"]
