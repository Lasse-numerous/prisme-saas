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
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

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


# Rate limiter - keyed by user ID from request state
def get_user_key(request: Request) -> str:
    """Get rate limit key from authenticated user."""
    user = getattr(request.state, "user", None)
    if user:
        return f"user:{user.id}"
    return get_remote_address(request)


limiter = Limiter(key_func=get_user_key)

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


def validate_port(port: int) -> str | None:
    """Validate port number.

    Returns error message if invalid, None if valid.
    Blocks privileged ports except 80 and 443.
    """
    if port < 1 or port > 65535:
        return "Port must be between 1 and 65535"
    if port < 1024 and port not in (80, 443):
        return f"Privileged port {port} not allowed. Use port 80, 443, or ports 1024-65535"
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
    port: int = 80


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
@limiter.limit("5/minute")
async def claim_subdomain(
    request: Request,
    db: DbSession,
    claim_request: SubdomainClaimRequest,
    current_user: CurrentActiveUser,
) -> SubdomainRead:
    """Claim a subdomain name (reserve it without IP).

    This reserves the subdomain name for later activation. The subdomain
    won't have a DNS record until activated with an IP address.
    """
    # Require verified email
    if not current_user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required before claiming subdomains",
        )

    name = claim_request.name.lower().strip()

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

    # Check if subdomain exists but is in cooldown period
    service = SubdomainService(db)
    existing = await service.get_by_name(name)
    if existing:
        if existing.cooldown_until and existing.cooldown_until > datetime.now(UTC):
            days_remaining = (existing.cooldown_until - datetime.now(UTC)).days
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Subdomain '{name}' is in cooldown period. Available in {days_remaining} days.",
            )
        # If past cooldown, subdomain can be claimed
        if existing.status == "released":
            # Delete the released record so it can be re-claimed
            await service.delete(id=existing.id, soft=False)
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Subdomain '{name}' is already claimed",
            )

    # Check user's subdomain limit
    user_subdomains = await service.count_filtered(
        filters=SubdomainFilter(owner_id=current_user.id)
    )
    if user_subdomains >= current_user.subdomain_limit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Subdomain limit reached ({current_user.subdomain_limit})",
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
@limiter.limit("10/hour")
async def activate_subdomain(
    request: Request,
    db: DbSession,
    name: str,
    activate_request: SubdomainActivateRequest,
    current_user: CurrentActiveUser,
) -> SubdomainRead:
    """Activate a subdomain by setting its IP address and creating DNS record.

    This creates an A record pointing to the provided IP address.
    Users can only activate their own subdomains.
    """
    # Validate IP address format first
    ip_error = validate_ip_address(activate_request.ip_address)
    if ip_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ip_error,
        )

    # Validate port
    port_error = validate_port(activate_request.port)
    if port_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=port_error,
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
                await dns_service.update_a_record(dns_record_id, activate_request.ip_address)
                logger.info(f"DNS record updated for {name}: {activate_request.ip_address}")
            else:
                # Create new record
                dns_record_id = await dns_service.create_a_record(
                    name.lower(), activate_request.ip_address
                )
                logger.info(f"DNS record created for {name}: {activate_request.ip_address}")
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
        ip_address=activate_request.ip_address,
        port=activate_request.port,
        status="active",
        dns_record_id=dns_record_id,
    )
    result = await service.update(id=subdomain.id, data=update_data)

    # Create Traefik route
    from prisme_api.services.route_manager import get_route_manager

    route_manager = get_route_manager()
    if route_manager:
        try:
            await route_manager.create_route(
                name.lower(),
                activate_request.ip_address,
                activate_request.port,
            )
        except Exception as e:
            logger.error(f"Failed to create route for {name}: {e}")
            # Continue - DNS is primary, route is secondary

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

    # Delete Traefik route first
    from prisme_api.services.route_manager import get_route_manager

    route_manager = get_route_manager()
    if route_manager:
        try:
            await route_manager.delete_route(name.lower())
        except Exception as e:
            logger.error(f"Failed to delete route for {name}: {e}")

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

    # Instead of deleting, update to released status with cooldown
    cooldown_days = 30
    now = datetime.now(UTC)
    update_data = SubdomainUpdate(
        status="released",
        ip_address=None,
        dns_record_id=None,
        owner_id=None,
        released_at=now,
        cooldown_until=now + timedelta(days=cooldown_days),
    )
    await service.update(id=subdomain.id, data=update_data)
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
