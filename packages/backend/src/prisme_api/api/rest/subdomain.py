"""Custom REST API routes for Subdomain.

This file extends the base routes with:
- Owner-based access control (users see their own, admins see all)
- Reserved name validation
- Hetzner DNS integration
- DNS propagation status endpoint
"""

from __future__ import annotations

import logging
import re
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from prisme_api.auth.dependencies import CurrentActiveUser, get_current_active_user
from prisme_api.schemas.base import PaginatedResponse
from prisme_api.schemas.subdomain import (
    SubdomainCreate,
    SubdomainFilter,
    SubdomainRead,
    SubdomainUpdate,
)
from prisme_api.services.hetzner_dns import (
    HetznerDNSError,
    HetznerDNSService,
    is_reserved_subdomain,
)
from prisme_api.services.subdomain import SubdomainService

from ._generated.deps import DbSession, Pagination, Sorting

logger = logging.getLogger(__name__)

# Subdomain validation pattern
SUBDOMAIN_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$")


def validate_subdomain_name(name: str) -> str | None:
    """Validate subdomain name.

    Returns error message if invalid, None if valid.
    """
    if len(name) < 3:
        return "Subdomain name must be at least 3 characters"
    if len(name) > 63:
        return "Subdomain name cannot exceed 63 characters"
    if not SUBDOMAIN_PATTERN.match(name):
        return (
            "Subdomain name must start and end with alphanumeric characters, "
            "and contain only lowercase letters, numbers, and hyphens"
        )
    return None


def validate_ip_address(ip: str) -> str | None:
    """Validate IPv4 address.

    Returns error message if invalid, None if valid.
    """
    pattern = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
    if not pattern.match(ip):
        return "Invalid IP address format"
    # Validate octets are 0-255
    octets = ip.split(".")
    for octet in octets:
        if not 0 <= int(octet) <= 255:
            return "Invalid IP address: octets must be 0-255"
    return None


# Create a new router with authentication required
router = APIRouter(
    prefix="/subdomains",
    tags=["subdomains"],
    dependencies=[Depends(get_current_active_user)],
)


class PropagationStatus(BaseModel):
    """DNS propagation status response."""

    subdomain: str
    ip_address: str | None
    status: str
    dns_record_id: str | None
    propagation: dict[str, bool]


class SubdomainClaimRequest(BaseModel):
    """Request to claim a subdomain."""

    name: str


class SubdomainActivateRequest(BaseModel):
    """Request to activate a subdomain with an IP address."""

    ip_address: str


def get_dns_service() -> HetznerDNSService | None:
    """Get the Hetzner DNS service if configured.

    Returns None if environment variables are not set (for local development).
    """
    try:
        return HetznerDNSService()
    except HetznerDNSError:
        logger.warning(
            "Hetzner DNS not configured - DNS operations will be skipped. "
            "Set HETZNER_DNS_API_TOKEN and HETZNER_DNS_ZONE_ID to enable."
        )
        return None


@router.get(
    "",
    response_model=PaginatedResponse[SubdomainRead],
    summary="List subdomains",
)
async def list_subdomains(
    db: DbSession,
    current_user: CurrentActiveUser,
    pagination: Pagination,
    sorting: Sorting,
) -> PaginatedResponse[SubdomainRead]:
    """List subdomains - users see only their own, admins see all."""
    service = SubdomainService(db)

    # Apply owner filter for non-admin users
    filters = None
    if "admin" not in (current_user.roles or []):
        filters = SubdomainFilter(owner_id=current_user.id)

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
        items=[SubdomainRead.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=pages,
    )


@router.get(
    "/{id}",
    response_model=SubdomainRead,
    summary="Get subdomain",
)
async def get_subdomain(
    db: DbSession,
    id: int,
    current_user: CurrentActiveUser,
) -> SubdomainRead:
    """Get a subdomain by ID - users can only access their own."""
    service = SubdomainService(db)

    result = await service.get(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subdomain not found",
        )

    # Check ownership for non-admin users
    if "admin" not in (current_user.roles or []) and result.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return SubdomainRead.model_validate(result)


@router.post(
    "/claim",
    response_model=SubdomainRead,
    status_code=status.HTTP_201_CREATED,
    summary="Claim a subdomain",
)
async def claim_subdomain(
    db: DbSession,
    request: SubdomainClaimRequest,
    current_user: CurrentActiveUser,
) -> SubdomainRead:
    """Claim a subdomain name (reserve it without IP).

    This reserves the subdomain name for later activation. The subdomain
    won't have a DNS record until activated with an IP address.
    """
    name = request.name.lower().strip()

    # Validate subdomain name format
    validation_error = validate_subdomain_name(name)
    if validation_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation_error,
        )

    # Validate reserved names
    if is_reserved_subdomain(name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Subdomain '{name}' is reserved and cannot be claimed",
        )

    # Check if already exists
    service = SubdomainService(db)
    existing = await service.get_by_name(name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Subdomain '{name}' is already claimed",
        )

    # Create subdomain in reserved state, owned by current user
    data = SubdomainCreate(name=name, status="reserved", owner_id=current_user.id)
    result = await service.create(data=data)

    logger.info(f"Subdomain claimed: {name} by user {current_user.id}")
    return SubdomainRead.model_validate(result)


@router.post(
    "/{name}/activate",
    response_model=SubdomainRead,
    summary="Activate a subdomain with IP address",
)
async def activate_subdomain(
    db: DbSession,
    name: str,
    request: SubdomainActivateRequest,
    current_user: CurrentActiveUser,
) -> SubdomainRead:
    """Activate a subdomain by setting its IP address and creating DNS record.

    This creates an A record pointing to the provided IP address.
    Users can only activate their own subdomains.
    """
    # Validate IP address format first
    ip_error = validate_ip_address(request.ip_address)
    if ip_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ip_error,
        )

    service = SubdomainService(db)

    # Get subdomain by name
    subdomain = await service.get_by_name(name.lower())
    if not subdomain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subdomain '{name}' not found",
        )

    # Check ownership for non-admin users
    if "admin" not in (current_user.roles or []) and subdomain.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    if subdomain.status == "suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Subdomain is suspended",
        )

    # Create or update DNS record
    dns_service = get_dns_service()
    dns_record_id = subdomain.dns_record_id

    if dns_service:
        try:
            if dns_record_id:
                # Update existing record
                await dns_service.update_a_record(dns_record_id, request.ip_address)
                logger.info(f"DNS record updated for {name}: {request.ip_address}")
            else:
                # Create new record
                dns_record_id = await dns_service.create_a_record(name.lower(), request.ip_address)
                logger.info(f"DNS record created for {name}: {request.ip_address}")
        except HetznerDNSError as e:
            logger.error(f"DNS error for {name}: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to update DNS record: {e!s}",
            ) from e
        finally:
            await dns_service.close()

    # Update subdomain
    update_data = SubdomainUpdate(
        ip_address=request.ip_address,
        status="active",
        dns_record_id=dns_record_id,
    )
    result = await service.update(id=subdomain.id, data=update_data)

    return SubdomainRead.model_validate(result)


@router.get(
    "/{name}/status",
    response_model=PropagationStatus,
    summary="Get subdomain DNS propagation status",
)
async def get_subdomain_status(
    db: DbSession,
    name: str,
    current_user: CurrentActiveUser,
) -> PropagationStatus:
    """Check DNS propagation status for a subdomain.

    Returns the current status and whether the DNS record has propagated
    to major DNS resolvers. Users can only check their own subdomains.
    """
    service = SubdomainService(db)

    subdomain = await service.get_by_name(name.lower())
    if not subdomain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subdomain '{name}' not found",
        )

    # Check ownership for non-admin users
    if "admin" not in (current_user.roles or []) and subdomain.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    propagation = {}
    if subdomain.ip_address:
        dns_service = get_dns_service()
        if dns_service:
            propagation = dns_service.check_propagation(name.lower(), subdomain.ip_address)
            await dns_service.close()

    return PropagationStatus(
        subdomain=subdomain.name,
        ip_address=subdomain.ip_address,
        status=subdomain.status,
        dns_record_id=subdomain.dns_record_id,
        propagation=propagation,
    )


@router.post(
    "/{name}/release",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Release a subdomain",
)
async def release_subdomain(
    db: DbSession,
    name: str,
    current_user: CurrentActiveUser,
) -> None:
    """Release a subdomain and delete its DNS record.

    This deletes the DNS record and marks the subdomain as released.
    Users can only release their own subdomains.
    """
    service = SubdomainService(db)

    subdomain = await service.get_by_name(name.lower())
    if not subdomain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subdomain '{name}' not found",
        )

    # Check ownership for non-admin users
    if "admin" not in (current_user.roles or []) and subdomain.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    # Delete DNS record if exists
    if subdomain.dns_record_id:
        dns_service = get_dns_service()
        if dns_service:
            try:
                await dns_service.delete_a_record(subdomain.dns_record_id)
                logger.info(f"DNS record deleted for {name}")
            except HetznerDNSError as e:
                logger.error(f"Failed to delete DNS record for {name}: {e}")
                # Continue with release even if DNS deletion fails
            finally:
                await dns_service.close()

    # Delete subdomain from database
    await service.delete(id=subdomain.id, soft=False)
    logger.info(f"Subdomain released: {name}")


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete subdomain",
)
async def delete_subdomain(
    db: DbSession,
    id: int,
    current_user: CurrentActiveUser,
    hard: Annotated[bool, Query(description="Permanently delete")] = False,
) -> None:
    """Delete a subdomain - users can only delete their own."""
    service = SubdomainService(db)

    existing = await service.get(id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subdomain not found",
        )

    # Check ownership for non-admin users
    if "admin" not in (current_user.roles or []) and existing.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    # Delete DNS record if exists
    if existing.dns_record_id:
        dns_service = get_dns_service()
        if dns_service:
            try:
                await dns_service.delete_a_record(existing.dns_record_id)
                logger.info(f"DNS record deleted for subdomain {id}")
            except HetznerDNSError as e:
                logger.error(f"Failed to delete DNS record for subdomain {id}: {e}")
            finally:
                await dns_service.close()

    await service.delete(id=id, soft=not hard)


__all__ = ["router"]
