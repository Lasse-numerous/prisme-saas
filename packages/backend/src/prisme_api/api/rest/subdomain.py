"""Custom REST API routes for Subdomain.

This file extends the base routes with:
- API key authentication
- Reserved name validation
- Hetzner DNS integration
- DNS propagation status endpoint
"""

from __future__ import annotations

import logging
import re

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from prisme_api.middleware.api_key import APIKey, get_api_key
from prisme_api.schemas.subdomain import (
    SubdomainCreate,
    SubdomainRead,
    SubdomainUpdate,
)
from prisme_api.services.hetzner_dns import (
    HetznerDNSError,
    HetznerDNSService,
    is_reserved_subdomain,
)
from prisme_api.services.subdomain import SubdomainService

from ._generated.deps import DbSession
from ._generated.subdomain_routes import router as base_router

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
router = APIRouter(dependencies=[Depends(get_api_key)])

# Include base routes (they will inherit the authentication dependency)
router.include_router(base_router)


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


@router.post(
    "/subdomains/claim",
    response_model=SubdomainRead,
    status_code=status.HTTP_201_CREATED,
    summary="Claim a subdomain",
)
async def claim_subdomain(
    db: DbSession,
    request: SubdomainClaimRequest,
    api_key: APIKey,
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

    # Create subdomain in reserved state
    data = SubdomainCreate(name=name, status="reserved")
    result = await service.create(data=data)

    logger.info(f"Subdomain claimed: {name}")
    return SubdomainRead.model_validate(result)


@router.post(
    "/subdomains/{name}/activate",
    response_model=SubdomainRead,
    summary="Activate a subdomain with IP address",
)
async def activate_subdomain(
    db: DbSession,
    name: str,
    request: SubdomainActivateRequest,
    api_key: APIKey,
) -> SubdomainRead:
    """Activate a subdomain by setting its IP address and creating DNS record.

    This creates an A record pointing to the provided IP address.
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
    "/subdomains/{name}/status",
    response_model=PropagationStatus,
    summary="Get subdomain DNS propagation status",
)
async def get_subdomain_status(
    db: DbSession,
    name: str,
    api_key: APIKey,
) -> PropagationStatus:
    """Check DNS propagation status for a subdomain.

    Returns the current status and whether the DNS record has propagated
    to major DNS resolvers.
    """
    service = SubdomainService(db)

    subdomain = await service.get_by_name(name.lower())
    if not subdomain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subdomain '{name}' not found",
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
    "/subdomains/{name}/release",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Release a subdomain",
)
async def release_subdomain(
    db: DbSession,
    name: str,
    api_key: APIKey,
) -> None:
    """Release a subdomain and delete its DNS record.

    This deletes the DNS record and marks the subdomain as released.
    """
    service = SubdomainService(db)

    subdomain = await service.get_by_name(name.lower())
    if not subdomain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subdomain '{name}' not found",
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


__all__ = ["router"]
