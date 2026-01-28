# Code Override Log

**Last Updated**: 2026-01-28T18:58:10.254619

**Unreviewed Overrides**: 6


---


## ⚠️ packages/frontend/src/router.tsx

**Strategy**: merge
**Status**: Not Reviewed
**Changes**: +6 lines, -4 lines, ~63 lines
**Last Modified**: 2026-01-28T18:58:10.254594

### What Changed

<details>
<summary>Show Diff</summary>

*Diff not available (run generation again to regenerate)*


</details>

### Actions

- Review your custom code to ensure it's still compatible
- Run `prism test` to verify functionality
- Run `prism review mark-reviewed packages/frontend/src/router.tsx` when done

---


## ⚠️ packages/backend/src/prisme_api/api/rest/subdomain.py

**Strategy**: generate_once
**Status**: Not Reviewed
**Changes**: +0 lines, -0 lines, ~559 lines
**Last Modified**: 2026-01-28T18:58:09.621469

### What Changed

<details>
<summary>Show Diff</summary>

```diff
--- generated+++ user@@ -1,26 +1,568 @@ """Custom REST API routes for Subdomain.

-✅ YOUR CODE - Safe to modify, will not be overwritten.
-This file was generated once by Prism and is yours to customize.
+This file extends the base routes with:
+- Owner-based access control (users see their own, admins see all)
+- Reserved name validation
+- Hetzner DNS integration
+- DNS propagation status endpoint
 """

 from __future__ import annotations

-from fastapi import APIRouter
-
-from ._generated.subdomain_routes import router as base_router
-
-# Create a new router that includes the base routes
-router = APIRouter()
-router.include_router(base_router)
-
-
-# Add your custom endpoints below
-# Example:
-# @router.get("/subdomains/stats")
-# async def get_subdomain_stats(db: DbSession):
-#     """Get statistics for subdomains."""
-#     pass
+import logging
+import re
+from datetime import UTC, datetime, timedelta
+from typing import Annotated
+
+from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
+from pydantic import BaseModel
+from slowapi import Limiter
+from slowapi.util import get_remote_address
+
+from prisme_api.auth.dependencies import CurrentActiveUser, get_current_active_user
+from prisme_api.schemas.base import PaginatedResponse
+from prisme_api.schemas.subdomain import (
+    SubdomainCreate,
+    SubdomainFilter,
+    SubdomainRead,
+    SubdomainUpdate,
+)
+from prisme_api.services.hetzner_dns import (
+    HetznerDNSError,
+    HetznerDNSService,
+    is_reserved_subdomain,
+)
+from prisme_api.services.subdomain import SubdomainService
+
+from ._generated.deps import DbSession, Pagination, Sorting
+
+logger = logging.getLogger(__name__)
+
+
+# Rate limiter - keyed by user ID from request state
+def get_user_key(request: Request) -> str:
+    """Get rate limit key from authenticated user."""
+    user = getattr(request.state, "user", None)
+    if user:
+        return f"user:{user.id}"
+    return get_remote_address(request)
+
+
+limiter = Limiter(key_func=get_user_key)
+
+# Subdomain validation pattern
+SUBDOMAIN_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$")
+
+
+def validate_subdomain_name(name: str) -> str | None:
+    """Validate subdomain name.
+
+    Returns error message if invalid, None if valid.
+    """
+    if len(name) < 3:
+        return "Subdomain name must be at least 3 characters"
+    if len(name) > 63:
+        return "Subdomain name cannot exceed 63 characters"
+    if not SUBDOMAIN_PATTERN.match(name):
+        return (
+            "Subdomain name must start and end with alphanumeric characters, "
+            "and contain only lowercase letters, numbers, and hyphens"
+        )
+    return None
+
+
+def validate_ip_address(ip: str) -> str | None:
+    """Validate IPv4 address.
+
+    Returns error message if invalid, None if valid.
+    """
+    pattern = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
+    if not pattern.match(ip):
+        return "Invalid IP address format"
+    # Validate octets are 0-255
+    octets = ip.split(".")
+    for octet in octets:
+        if not 0 <= int(octet) <= 255:
+            return "Invalid IP address: octets must be 0-255"
+    return None
+
+
+def validate_port(port: int) -> str | None:
+    """Validate port number.
+
+    Returns error message if invalid, None if valid.
+    Blocks privileged ports except 80 and 443.
+    """
+    if port < 1 or port > 65535:
+        return "Port must be between 1 and 65535"
+    if port < 1024 and port not in (80, 443):
+        return f"Privileged port {port} not allowed. Use port 80, 443, or ports 1024-65535"
+    return None
+
+
+# Create a new router with authentication required
+router = APIRouter(
+    prefix="/subdomains",
+    tags=["subdomains"],
+    dependencies=[Depends(get_current_active_user)],
+)
+
+
+class PropagationStatus(BaseModel):
+    """DNS propagation status response."""
+
+    subdomain: str
+    ip_address: str | None
+    status: str
+    dns_record_id: str | None
+    propagation: dict[str, bool]
+
+
+class SubdomainClaimRequest(BaseModel):
+    """Request to claim a subdomain."""
+
+    name: str
+
+
+class SubdomainActivateRequest(BaseModel):
+    """Request to activate a subdomain with an IP address."""
+
+    ip_address: str
+    port: int = 80
+
+
+def get_dns_service() -> HetznerDNSService | None:
+    """Get the Hetzner DNS service if configured.
+
+    Returns None if environment variables are not set (for local development).
+    """
+    try:
+        return HetznerDNSService()
+    except HetznerDNSError:
+        logger.warning(
+            "Hetzner DNS not configured - DNS operations will be skipped. "
+            "Set HETZNER_DNS_API_TOKEN and HETZNER_DNS_ZONE_ID to enable."
+        )
+        return None
+
+
+@router.get(
+    "",
+    response_model=PaginatedResponse[SubdomainRead],
+    summary="List subdomains",
+)
+async def list_subdomains(
+    db: DbSession,
+    current_user: CurrentActiveUser,
+    pagination: Pagination,
+    sorting: Sorting,
+) -> PaginatedResponse[SubdomainRead]:
+    """List subdomains - users see only their own, admins see all."""
+    service = SubdomainService(db)
+
+    # Apply owner filter for non-admin users
+    filters = None
+    if "admin" not in (current_user.roles or []):
+        filters = SubdomainFilter(owner_id=current_user.id)
+
+    items = await service.list(
+        skip=pagination.skip,
+        limit=pagination.limit,
+        sort_by=sorting.sort_by,
+        sort_order=sorting.sort_order,
+        filters=filters,
+    )
+
+    total = await service.count_filtered(filters=filters)
+    pages = (
+        (total + pagination.page_size - 1) // pagination.page_size if pagination.page_size else 1
+    )
+
+    return PaginatedResponse(
+        items=[SubdomainRead.model_validate(item) for item in items],
+        total=total,
+        page=pagination.page,
+        page_size=pagination.page_size,
+        pages=pages,
+    )
+
+
+@router.get(
+    "/{id}",
+    response_model=SubdomainRead,
+    summary="Get subdomain",
+)
+async def get_subdomain(
+    db: DbSession,
+    id: int,
+    current_user: CurrentActiveUser,
+) -> SubdomainRead:
+    """Get a subdomain by ID - users can only access their own."""
+    service = SubdomainService(db)
+
+    result = await service.get(id)
+    if result is None:
+        raise HTTPException(
+            status_code=status.HTTP_404_NOT_FOUND,
+            detail="Subdomain not found",
+        )
+
+    # Check ownership for non-admin users
+    if "admin" not in (current_user.roles or []) and result.owner_id != current_user.id:
+        raise HTTPException(
+            status_code=status.HTTP_403_FORBIDDEN,
+            detail="Access denied",
+        )
+
+    return SubdomainRead.model_validate(result)
+
+
+@router.post(
+    "/claim",
+    response_model=SubdomainRead,
+    status_code=status.HTTP_201_CREATED,
+    summary="Claim a subdomain",
+)
+@limiter.limit("5/minute")
+async def claim_subdomain(
+    request: Request,
+    db: DbSession,
+    claim_request: SubdomainClaimRequest,
+    current_user: CurrentActiveUser,
+) -> SubdomainRead:
+    """Claim a subdomain name (reserve it without IP).
+
+    This reserves the subdomain name for later activation. The subdomain
+    won't have a DNS record until activated with an IP address.
+    """
+    # Require verified email
+    if not current_user.email_verified:
+        raise HTTPException(
+            status_code=status.HTTP_403_FORBIDDEN,
+            detail="Email verification required before claiming subdomains",
+        )
+
+    name = claim_request.name.lower().strip()
+
+    # Validate subdomain name format
+    validation_error = validate_subdomain_name(name)
+    if validation_error:
+        raise HTTPException(
+            status_code=status.HTTP_400_BAD_REQUEST,
+            detail=validation_error,
+        )
+
+    # Validate reserved names
+    if is_reserved_subdomain(name):
+        raise HTTPException(
+            status_code=status.HTTP_400_BAD_REQUEST,
+            detail=f"Subdomain '{name}' is reserved and cannot be claimed",
+        )
+
+    # Check if subdomain exists but is in cooldown period
+    service = SubdomainService(db)
+    existing = await service.get_by_name(name)
+    if existing:
+        if existing.cooldown_until and existing.cooldown_until > datetime.now(UTC):
+            days_remaining = (existing.cooldown_until - datetime.now(UTC)).days
+            raise HTTPException(
+                status_code=status.HTTP_409_CONFLICT,
+                detail=f"Subdomain '{name}' is in cooldown period. Available in {days_remaining} days.",
+            )
+        # If past cooldown, subdomain can be claimed
+        if existing.status == "released":
+            # Delete the released record so it can be re-claimed
+            await service.delete(id=existing.id, soft=False)
+        else:
+            raise HTTPException(
+                status_code=status.HTTP_409_CONFLICT,
+                detail=f"Subdomain '{name}' is already claimed",
+            )
+
+    # Check user's subdomain limit
+    user_subdomains = await service.count_filtered(
+        filters=SubdomainFilter(owner_id=current_user.id)
+    )
+    if user_subdomains >= current_user.subdomain_limit:
+        raise HTTPException(
+            status_code=status.HTTP_403_FORBIDDEN,
+            detail=f"Subdomain limit reached ({current_user.subdomain_limit})",
+        )
+
+    # Create subdomain in reserved state, owned by current user
+    data = SubdomainCreate(name=name, status="reserved", owner_id=current_user.id)
+    result = await service.create(data=data)
+
+    logger.info(f"Subdomain claimed: {name} by user {current_user.id}")
+    return SubdomainRead.model_validate(result)
+
+
+@router.post(
+    "/{name}/activate",
+    response_model=SubdomainRead,
+    summary="Activate a subdomain with IP address",
+)
+@limiter.limit("10/hour")
+async def activate_subdomain(
+    request: Request,
+    db: DbSession,
+    name: str,
+    activate_request: SubdomainActivateRequest,
+    current_user: CurrentActiveUser,
+) -> SubdomainRead:
+    """Activate a subdomain by setting its IP address and creating DNS record.
+
+    This creates an A record pointing to the provided IP address.
+    Users can only activate their own subdomains.
+    """
+    # Validate IP address format first
+    ip_error = validate_ip_address(activate_request.ip_address)
+    if ip_error:
+        raise HTTPException(
+            status_code=status.HTTP_400_BAD_REQUEST,
+            detail=ip_error,
+        )
+
+    # Validate port
+    port_error = validate_port(activate_request.port)
+    if port_error:
+        raise HTTPException(
+            status_code=status.HTTP_400_BAD_REQUEST,
+            detail=port_error,
+        )
+
+    service = SubdomainService(db)
+
+    # Get subdomain by name
+    subdomain = await service.get_by_name(name.lower())
+    if not subdomain:
+        raise HTTPException(
+            status_code=status.HTTP_404_NOT_FOUND,
+            detail=f"Subdomain '{name}' not found",
+        )
+
+    # Check ownership for non-admin users
+    if "admin" not in (current_user.roles or []) and subdomain.owner_id != current_user.id:
+        raise HTTPException(
+            status_code=status.HTTP_403_FORBIDDEN,
+            detail="Access denied",
+        )
+
+    if subdomain.status == "suspended":
+        raise HTTPException(
+            status_code=status.HTTP_403_FORBIDDEN,
+            detail="Subdomain is suspended",
+        )
+
+    # Create or update DNS record
+    dns_service = get_dns_service()
+    dns_record_id = subdomain.dns_record_id
+
+    if dns_service:
+        try:
+            if dns_record_id:
+                # Update existing record
+                await dns_service.update_a_record(dns_record_id, activate_request.ip_address)
+                logger.info(f"DNS record updated for {name}: {activate_request.ip_address}")
+            else:
+                # Create new record
+                dns_record_id = await dns_service.create_a_record(
+                    name.lower(), activate_request.ip_address
+                )
+                logger.info(f"DNS record created for {name}: {activate_request.ip_address}")
+        except HetznerDNSError as e:
+            logger.error(f"DNS error for {name}: {e}")
+            raise HTTPException(
+                status_code=status.HTTP_502_BAD_GATEWAY,
+                detail=f"Failed to update DNS record: {e!s}",
+            ) from e
+        finally:
+            await dns_service.close()
+
+    # Update subdomain
+    update_data = SubdomainUpdate(
+        ip_address=activate_request.ip_address,
+        port=activate_request.port,
+        status="active",
+        dns_record_id=dns_record_id,
+    )
+    result = await service.update(id=subdomain.id, data=update_data)
+
+    # Create Traefik route
+    from prisme_api.services.route_manager import get_route_manager
+
+    route_manager = get_route_manager()
+    if route_manager:
+        try:
+            await route_manager.create_route(
+                name.lower(),
+                activate_request.ip_address,
+                activate_request.port,
+            )
+        except Exception as e:
+            logger.error(f"Failed to create route for {name}: {e}")
+            # Continue - DNS is primary, route is secondary
+
+    return SubdomainRead.model_validate(result)
+
+
+@router.get(
+    "/{name}/status",
+    response_model=PropagationStatus,
+    summary="Get subdomain DNS propagation status",
+)
+async def get_subdomain_status(
+    db: DbSession,
+    name: str,
+    current_user: CurrentActiveUser,
+) -> PropagationStatus:
+    """Check DNS propagation status for a subdomain.
+
+    Returns the current status and whether the DNS record has propagated
+    to major DNS resolvers. Users can only check their own subdomains.
+    """
+    service = SubdomainService(db)
+
+    subdomain = await service.get_by_name(name.lower())
+    if not subdomain:
+        raise HTTPException(
+            status_code=status.HTTP_404_NOT_FOUND,
+            detail=f"Subdomain '{name}' not found",
+        )
+
+    # Check ownership for non-admin users
+    if "admin" not in (current_user.roles or []) and subdomain.owner_id != current_user.id:
+        raise HTTPException(
+            status_code=status.HTTP_403_FORBIDDEN,
+            detail="Access denied",
+        )
+
+    propagation = {}
+    if subdomain.ip_address:
+        dns_service = get_dns_service()
+        if dns_service:
+            propagation = dns_service.check_propagation(name.lower(), subdomain.ip_address)
+            await dns_service.close()
+
+    return PropagationStatus(
+        subdomain=subdomain.name,
+        ip_address=subdomain.ip_address,
+        status=subdomain.status,
+        dns_record_id=subdomain.dns_record_id,
+        propagation=propagation,
+    )
+
+
+@router.post(
+    "/{name}/release",
+    status_code=status.HTTP_204_NO_CONTENT,
+    summary="Release a subdomain",
+)
+async def release_subdomain(
+    db: DbSession,
+    name: str,
+    current_user: CurrentActiveUser,
+) -> None:
+    """Release a subdomain and delete its DNS record.
+
+    This deletes the DNS record and marks the subdomain as released.
+    Users can only release their own subdomains.
+    """
+    service = SubdomainService(db)
+
+    subdomain = await service.get_by_name(name.lower())
+    if not subdomain:
+        raise HTTPException(
+            status_code=status.HTTP_404_NOT_FOUND,
+            detail=f"Subdomain '{name}' not found",
+        )
+
+    # Check ownership for non-admin users
+    if "admin" not in (current_user.roles or []) and subdomain.owner_id != current_user.id:
+        raise HTTPException(
+            status_code=status.HTTP_403_FORBIDDEN,
+            detail="Access denied",
+        )
+
+    # Delete Traefik route first
+    from prisme_api.services.route_manager import get_route_manager
+
+    route_manager = get_route_manager()
+    if route_manager:
+        try:
+            await route_manager.delete_route(name.lower())
+        except Exception as e:
+            logger.error(f"Failed to delete route for {name}: {e}")
+
+    # Delete DNS record if exists
+    if subdomain.dns_record_id:
+        dns_service = get_dns_service()
+        if dns_service:
+            try:
+                await dns_service.delete_a_record(subdomain.dns_record_id)
+                logger.info(f"DNS record deleted for {name}")
+            except HetznerDNSError as e:
+                logger.error(f"Failed to delete DNS record for {name}: {e}")
+                # Continue with release even if DNS deletion fails
+            finally:
+                await dns_service.close()
+
+    # Instead of deleting, update to released status with cooldown
+    cooldown_days = 30
+    now = datetime.now(UTC)
+    update_data = SubdomainUpdate(
+        status="released",
+        ip_address=None,
+        dns_record_id=None,
+        owner_id=None,
+        released_at=now,
+        cooldown_until=now + timedelta(days=cooldown_days),
+    )
+    await service.update(id=subdomain.id, data=update_data)
+    logger.info(f"Subdomain released: {name}")
+
+
+@router.delete(
+    "/{id}",
+    status_code=status.HTTP_204_NO_CONTENT,
+    summary="Delete subdomain",
+)
+async def delete_subdomain(
+    db: DbSession,
+    id: int,
+    current_user: CurrentActiveUser,
+    hard: Annotated[bool, Query(description="Permanently delete")] = False,
+) -> None:
+    """Delete a subdomain - users can only delete their own."""
+    service = SubdomainService(db)
+
+    existing = await service.get(id)
+    if existing is None:
+        raise HTTPException(
+            status_code=status.HTTP_404_NOT_FOUND,
+            detail="Subdomain not found",
+        )
+
+    # Check ownership for non-admin users
+    if "admin" not in (current_user.roles or []) and existing.owner_id != current_user.id:
+        raise HTTPException(
+            status_code=status.HTTP_403_FORBIDDEN,
+            detail="Access denied",
+        )
+
+    # Delete DNS record if exists
+    if existing.dns_record_id:
+        dns_service = get_dns_service()
+        if dns_service:
+            try:
+                await dns_service.delete_a_record(existing.dns_record_id)
+                logger.info(f"DNS record deleted for subdomain {id}")
+            except HetznerDNSError as e:
+                logger.error(f"Failed to delete DNS record for subdomain {id}: {e}")
+            finally:
+                await dns_service.close()
+
+    await service.delete(id=id, soft=not hard)


 __all__ = ["router"]

```

</details>

### Actions

- Review your custom code to ensure it's still compatible
- Run `prism test` to verify functionality
- Run `prism review mark-reviewed packages/backend/src/prisme_api/api/rest/subdomain.py` when done

---


## ⚠️ packages/backend/src/prisme_api/api/rest/api_key.py

**Strategy**: generate_once
**Status**: Not Reviewed
**Changes**: +4 lines, -0 lines, ~178 lines
**Last Modified**: 2026-01-28T18:58:09.616627

### What Changed

<details>
<summary>Show Diff</summary>

```diff
--- generated+++ user@@ -2,25 +2,196 @@
 ✅ YOUR CODE - Safe to modify, will not be overwritten.
 This file was generated once by Prism and is yours to customize.
+
+Protected with owner-based access control:
+- Users can only access their own API keys
+- Admins can access all API keys
 """

 from __future__ import annotations

-from fastapi import APIRouter
+from typing import Annotated

-from ._generated.api_key_routes import router as base_router
+from fastapi import APIRouter, Depends, HTTPException, Query, status

-# Create a new router that includes the base routes
-router = APIRouter()
-router.include_router(base_router)
+from prisme_api.auth.dependencies import CurrentActiveUser, get_current_active_user
+from prisme_api.schemas.api_key import (
+    APIKeyCreate,
+    APIKeyFilter,
+    APIKeyRead,
+    APIKeyUpdate,
+)
+from prisme_api.schemas.base import PaginatedResponse
+from prisme_api.services.api_key import APIKeyService
+
+from ._generated.deps import DbSession, Pagination, Sorting
+
+# Create a new router with authentication required
+router = APIRouter(
+    prefix="/api-keys",
+    tags=["api-keys"],
+    dependencies=[Depends(get_current_active_user)],
+)


-# Add your custom endpoints below
-# Example:
-# @router.get("/api_keys/stats")
-# async def get_api_key_stats(db: DbSession):
-#     """Get statistics for api_keys."""
-#     pass
+@router.get(
+    "",
+    response_model=PaginatedResponse[APIKeyRead],
+    summary="List API keys",
+)
+async def list_api_keys(
+    db: DbSession,
+    current_user: CurrentActiveUser,
+    pagination: Pagination,
+    sorting: Sorting,
+) -> PaginatedResponse[APIKeyRead]:
+    """List API keys - users see only their own, admins see all."""
+    service = APIKeyService(db)
+
+    # Apply owner filter for non-admin users
+    filters = None
+    if "admin" not in (current_user.roles or []):
+        filters = APIKeyFilter(user_id=current_user.id)
+
+    items = await service.list(
+        skip=pagination.skip,
+        limit=pagination.limit,
+        sort_by=sorting.sort_by,
+        sort_order=sorting.sort_order,
+        filters=filters,
+    )
+
+    total = await service.count_filtered(filters=filters)
+    pages = (
+        (total + pagination.page_size - 1) // pagination.page_size if pagination.page_size else 1
+    )
+
+    return PaginatedResponse(
+        items=[APIKeyRead.model_validate(item) for item in items],
+        total=total,
+        page=pagination.page,
+        page_size=pagination.page_size,
+        pages=pages,
+    )
+
+
+@router.get(
+    "/{id}",
+    response_model=APIKeyRead,
+    summary="Get API key",
+)
+async def get_api_key(
+    db: DbSession,
+    id: int,
+    current_user: CurrentActiveUser,
+) -> APIKeyRead:
+    """Get an API key by ID - users can only access their own."""
+    service = APIKeyService(db)
+
+    result = await service.get(id)
+    if result is None:
+        raise HTTPException(
+            status_code=status.HTTP_404_NOT_FOUND,
+            detail="API key not found",
+        )
+
+    # Check ownership for non-admin users
+    if "admin" not in (current_user.roles or []) and result.user_id != current_user.id:
+        raise HTTPException(
+            status_code=status.HTTP_403_FORBIDDEN,
+            detail="Access denied",
+        )
+
+    return APIKeyRead.model_validate(result)
+
+
+@router.post(
+    "",
+    response_model=APIKeyRead,
+    status_code=status.HTTP_201_CREATED,
+    summary="Create API key",
+)
+async def create_api_key(
+    db: DbSession,
+    data: APIKeyCreate,
+    current_user: CurrentActiveUser,
+) -> APIKeyRead:
+    """Create a new API key - assigned to current user unless admin."""
+    service = APIKeyService(db)
+
+    # Non-admin users can only create keys for themselves
+    if "admin" not in (current_user.roles or []):
+        # Force user_id to current user
+        data = APIKeyCreate(
+            **data.model_dump(exclude={"user_id"}),
+            user_id=current_user.id,
+        )
+
+    result = await service.create(data=data)
+    return APIKeyRead.model_validate(result)
+
+
+@router.patch(
+    "/{id}",
+    response_model=APIKeyRead,
+    summary="Update API key",
+)
+async def update_api_key(
+    db: DbSession,
+    id: int,
+    data: APIKeyUpdate,
+    current_user: CurrentActiveUser,
+) -> APIKeyRead:
+    """Update an API key - users can only update their own."""
+    service = APIKeyService(db)
+
+    existing = await service.get(id)
+    if existing is None:
+        raise HTTPException(
+            status_code=status.HTTP_404_NOT_FOUND,
+            detail="API key not found",
+        )
+
+    # Check ownership for non-admin users
+    if "admin" not in (current_user.roles or []) and existing.user_id != current_user.id:
+        raise HTTPException(
+            status_code=status.HTTP_403_FORBIDDEN,
+            detail="Access denied",
+        )
+
+    result = await service.update(id=id, data=data)
+    return APIKeyRead.model_validate(result)
+
+
+@router.delete(
+    "/{id}",
+    status_code=status.HTTP_204_NO_CONTENT,
+    summary="Delete API key",
+)
+async def delete_api_key(
+    db: DbSession,
+    id: int,
+    current_user: CurrentActiveUser,
+    hard: Annotated[bool, Query(description="Permanently delete")] = False,
+) -> None:
+    """Delete an API key - users can only delete their own."""
+    service = APIKeyService(db)
+
+    existing = await service.get(id)
+    if existing is None:
+        raise HTTPException(
+            status_code=status.HTTP_404_NOT_FOUND,
+            detail="API key not found",
+        )
+
+    # Check ownership for non-admin users
+    if "admin" not in (current_user.roles or []) and existing.user_id != current_user.id:
+        raise HTTPException(
+            status_code=status.HTTP_403_FORBIDDEN,
+            detail="Access denied",
+        )
+
+    await service.delete(id=id, soft=not hard)


 __all__ = ["router"]

```

</details>

### Actions

- Review your custom code to ensure it's still compatible
- Run `prism test` to verify functionality
- Run `prism review mark-reviewed packages/backend/src/prisme_api/api/rest/api_key.py` when done

---


## ⚠️ packages/backend/src/prisme_api/api/rest/user.py

**Strategy**: generate_once
**Status**: Not Reviewed
**Changes**: +0 lines, -0 lines, ~8 lines
**Last Modified**: 2026-01-28T18:58:09.611618

### What Changed

<details>
<summary>Show Diff</summary>

```diff
--- generated+++ user@@ -6,12 +6,17 @@
 from __future__ import annotations

-from fastapi import APIRouter
+from fastapi import APIRouter, Depends
+
+from prisme_api.auth.dependencies import require_roles

 from ._generated.user_routes import router as base_router

-# Create a new router that includes the base routes
-router = APIRouter()
+# Create a new router with admin-only access
+# All user management endpoints require admin role
+router = APIRouter(
+    dependencies=[Depends(require_roles("admin"))],
+)
 router.include_router(base_router)



```

</details>

### Actions

- Review your custom code to ensure it's still compatible
- Run `prism test` to verify functionality
- Run `prism review mark-reviewed packages/backend/src/prisme_api/api/rest/user.py` when done

---


## ⚠️ packages/backend/src/prisme_api/api/rest/auth.py

**Strategy**: generate_once
**Status**: Not Reviewed
**Changes**: +20 lines, -0 lines, ~38 lines
**Last Modified**: 2026-01-28T18:58:09.579756

### What Changed

<details>
<summary>Show Diff</summary>

```diff
--- generated+++ user@@ -1,14 +1,17 @@ """Authentik authentication routes.

-AUTO-GENERATED BY PRISM - DO NOT EDIT
+⚠️ AUTO-GENERATED BY PRISM - DO NOT EDIT
 Endpoints for OIDC authentication flow with Authentik.
 """

 from __future__ import annotations

+import json
+import os
 import secrets
 from typing import Annotated

+import redis.asyncio as redis
 from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
 from fastapi.responses import RedirectResponse
 from sqlalchemy import select
@@ -23,8 +26,35 @@
 router = APIRouter(prefix="/auth", tags=["authentication"])

-# In-memory state store (use Redis in production for distributed systems)
-_state_store: dict[str, dict] = {}
+# Redis client for distributed state storage
+REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
+_redis_client: redis.Redis | None = None
+STATE_TTL = 600  # State expires after 10 minutes
+
+
+async def get_redis() -> redis.Redis:
+    """Get or create Redis client."""
+    global _redis_client
+    if _redis_client is None:
+        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
+    return _redis_client
+
+
+async def store_state(state: str, data: dict) -> None:
+    """Store state in Redis with TTL."""
+    client = await get_redis()
+    await client.setex(f"oauth_state:{state}", STATE_TTL, json.dumps(data))
+
+
+async def get_and_delete_state(state: str) -> dict | None:
+    """Get and delete state from Redis."""
+    client = await get_redis()
+    key = f"oauth_state:{state}"
+    data = await client.get(key)
+    if data:
+        await client.delete(key)
+        return json.loads(data)
+    return None


 @router.get("/login")
@@ -40,8 +70,8 @@     state = secrets.token_urlsafe(32)
     nonce = secrets.token_urlsafe(32)

-    # Store state and nonce for verification on callback
-    _state_store[state] = {"nonce": nonce}
+    # Store state and nonce in Redis for verification on callback
+    await store_state(state, {"nonce": nonce})

     authorization_url = oidc_client.get_authorization_url(
         state=state,
@@ -73,8 +103,8 @@     Raises:
         HTTPException: If state is invalid or token exchange fails
     """
-    # Verify state
-    stored = _state_store.pop(state, None)
+    # Verify state from Redis
+    stored = await get_and_delete_state(state)
     if not stored:
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
@@ -96,10 +126,22 @@
         # Get or create local user
         authentik_id = claims.get("sub")
-        result = await db.execute(
-            select(User).where(User.authentik_id == authentik_id)
-        )
+        result = await db.execute(select(User).where(User.authentik_id == authentik_id))
         user = result.scalar_one_or_none()
+
+        # Validate email domain against whitelist for new users
+        if not user:
+            from prisme_api.services.allowed_email_domain import AllowedEmailDomainService
+
+            email_domain_service = AllowedEmailDomainService(db)
+            email = claims.get("email", f"{claims.get('preferred_username', 'user')}@local")
+
+            if not await email_domain_service.is_domain_allowed(email):
+                domain = email.split("@")[1] if "@" in email else "unknown"
+                raise HTTPException(
+                    status_code=status.HTTP_403_FORBIDDEN,
+                    detail=f"Email domain '{domain}' is not allowed for signup. Contact admin for access.",
+                )

         if not user:
             # Create new user from claims
@@ -136,10 +178,13 @@         return response

     except OIDCError as e:
+        import logging
+
+        logging.error(f"OIDC authentication error: {e}")
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail=f"Authentication failed: {e}",
-        )
+        ) from e


 @router.get("/logout")

```

</details>

### Actions

- Review your custom code to ensure it's still compatible
- Run `prism test` to verify functionality
- Run `prism review mark-reviewed packages/backend/src/prisme_api/api/rest/auth.py` when done

---


## ⚠️ packages/backend/src/prisme_api/services/subdomain.py

**Strategy**: generate_once
**Status**: Not Reviewed
**Changes**: +4 lines, -0 lines, ~20 lines
**Last Modified**: 2026-01-28T18:58:09.546894

### What Changed

<details>
<summary>Show Diff</summary>

```diff
--- generated+++ user@@ -1,10 +1,13 @@ """Service for Subdomain.

-✅ YOUR CODE - Safe to modify, will not be overwritten.
-This file was generated once by Prism and is yours to customize.
+Custom service logic for managing subdomains with Hetzner DNS integration.
 """

 from __future__ import annotations
+
+from sqlalchemy import select
+
+from prisme_api.models.subdomain import Subdomain

 from ._generated.subdomain_base import SubdomainServiceBase

@@ -12,21 +15,23 @@ class SubdomainService(SubdomainServiceBase):
     """Custom service logic for Subdomain.

-    Add your custom methods and override base methods here.
+    Extends the base service with:
+    - Lookup by name (unique field)
+    - Subdomain validation
     """

-    # Example: Override a lifecycle hook
-    # async def before_create(self, data: SubdomainCreate) -> None:
-    #     # Custom validation or transformation
-    #     pass
+    async def get_by_name(self, name: str) -> Subdomain | None:
+        """Get a subdomain by its unique name.

-    # Example: Add a custom method
-    # async def find_by_email(self, email: str) -> Subdomain | None:
-    #     query = select(self.model).where(self.model.email == email)
-    #     result = await self.db.execute(query)
-    #     return result.scalar_one_or_none()
+        Args:
+            name: The subdomain name (e.g., 'myapp')

-    pass
+        Returns:
+            The Subdomain object if found, None otherwise
+        """
+        query = select(self.model).where(self.model.name == name.lower())
+        result = await self.db.execute(query)
+        return result.scalar_one_or_none()


 __all__ = ["SubdomainService"]

```

</details>

### Actions

- Review your custom code to ensure it's still compatible
- Run `prism test` to verify functionality
- Run `prism review mark-reviewed packages/backend/src/prisme_api/services/subdomain.py` when done

---
