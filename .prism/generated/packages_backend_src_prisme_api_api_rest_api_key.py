"""Custom REST API routes for APIKey.

✅ YOUR CODE - Safe to modify, will not be overwritten.
This file was generated once by Prism and is yours to customize.
"""

from __future__ import annotations

from fastapi import APIRouter

from ._generated.api_key_routes import router as base_router

# Create a new router that includes the base routes
router = APIRouter()
router.include_router(base_router)


# Add your custom endpoints below
# Example:
# @router.get("/api_keys/stats")
# async def get_api_key_stats(db: DbSession):
#     """Get statistics for api_keys."""
#     pass


__all__ = ["router"]
