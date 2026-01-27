"""Custom REST API routes for APIKey.

✅ YOUR CODE - Safe to modify, will not be overwritten.
This file was generated once by Prism and is yours to customize.

Protected with owner-based access control:
- Users can only access their own API keys
- Admins can access all API keys
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from prisme_api.auth.dependencies import CurrentActiveUser, get_current_active_user
from prisme_api.schemas.api_key import (
    APIKeyCreate,
    APIKeyFilter,
    APIKeyRead,
    APIKeyUpdate,
)
from prisme_api.schemas.base import PaginatedResponse
from prisme_api.services.api_key import APIKeyService

from ._generated.deps import DbSession, Pagination, Sorting

# Create a new router with authentication required
router = APIRouter(
    prefix="/api-keys",
    tags=["api-keys"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get(
    "",
    response_model=PaginatedResponse[APIKeyRead],
    summary="List API keys",
)
async def list_api_keys(
    db: DbSession,
    current_user: CurrentActiveUser,
    pagination: Pagination,
    sorting: Sorting,
) -> PaginatedResponse[APIKeyRead]:
    """List API keys - users see only their own, admins see all."""
    service = APIKeyService(db)

    # Apply owner filter for non-admin users
    filters = None
    if "admin" not in (current_user.roles or []):
        filters = APIKeyFilter(user_id=current_user.id)

    items = await service.list(
        skip=pagination.skip,
        limit=pagination.limit,
        sort_by=sorting.sort_by,
        sort_order=sorting.sort_order,
        filters=filters,
    )

    total = await service.count_filtered(filters=filters)
    pages = (
        (total + pagination.page_size - 1) // pagination.page_size if pagination.page_size else 1
    )

    return PaginatedResponse(
        items=[APIKeyRead.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=pages,
    )


@router.get(
    "/{id}",
    response_model=APIKeyRead,
    summary="Get API key",
)
async def get_api_key(
    db: DbSession,
    id: int,
    current_user: CurrentActiveUser,
) -> APIKeyRead:
    """Get an API key by ID - users can only access their own."""
    service = APIKeyService(db)

    result = await service.get(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )

    # Check ownership for non-admin users
    if "admin" not in (current_user.roles or []) and result.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return APIKeyRead.model_validate(result)


@router.post(
    "",
    response_model=APIKeyRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create API key",
)
async def create_api_key(
    db: DbSession,
    data: APIKeyCreate,
    current_user: CurrentActiveUser,
) -> APIKeyRead:
    """Create a new API key - assigned to current user unless admin."""
    service = APIKeyService(db)

    # Non-admin users can only create keys for themselves
    if "admin" not in (current_user.roles or []):
        # Force user_id to current user
        data = APIKeyCreate(
            **data.model_dump(exclude={"user_id"}),
            user_id=current_user.id,
        )

    result = await service.create(data=data)
    return APIKeyRead.model_validate(result)


@router.patch(
    "/{id}",
    response_model=APIKeyRead,
    summary="Update API key",
)
async def update_api_key(
    db: DbSession,
    id: int,
    data: APIKeyUpdate,
    current_user: CurrentActiveUser,
) -> APIKeyRead:
    """Update an API key - users can only update their own."""
    service = APIKeyService(db)

    existing = await service.get(id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )

    # Check ownership for non-admin users
    if "admin" not in (current_user.roles or []) and existing.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    result = await service.update(id=id, data=data)
    return APIKeyRead.model_validate(result)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete API key",
)
async def delete_api_key(
    db: DbSession,
    id: int,
    current_user: CurrentActiveUser,
    hard: Annotated[bool, Query(description="Permanently delete")] = False,
) -> None:
    """Delete an API key - users can only delete their own."""
    service = APIKeyService(db)

    existing = await service.get(id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )

    # Check ownership for non-admin users
    if "admin" not in (current_user.roles or []) and existing.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    await service.delete(id=id, soft=not hard)


__all__ = ["router"]
