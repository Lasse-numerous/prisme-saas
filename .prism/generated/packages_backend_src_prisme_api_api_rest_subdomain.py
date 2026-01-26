"""Custom REST API routes for Subdomain.

✅ YOUR CODE - Safe to modify, will not be overwritten.
This file was generated once by Prism and is yours to customize.
"""

from __future__ import annotations

from fastapi import APIRouter

from ._generated.subdomain_routes import router as base_router

# Create a new router that includes the base routes
router = APIRouter()
router.include_router(base_router)


# Add your custom endpoints below
# Example:
# @router.get("/subdomains/stats")
# async def get_subdomain_stats(db: DbSession):
#     """Get statistics for subdomains."""
#     pass


__all__ = ["router"]
