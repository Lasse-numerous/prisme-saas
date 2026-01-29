# Code Override Log

**Last Updated**: 2026-01-29T08:44:54.925055

**Unreviewed Overrides**: 6


---


## ⚠️ packages/frontend/src/router.tsx

**Strategy**: merge
**Status**: Not Reviewed
**Changes**: +5 lines, -4 lines, ~93 lines
**Last Modified**: 2026-01-29T08:44:54.925017

### What Changed

<details>
<summary>Show Diff</summary>

```diff
--- generated+++ user@@ -11,10 +11,9 @@ import { ThemeToggle } from './ui/ThemeToggle';
 import { Login } from './pages/Login';
 import { Signup } from './pages/Signup';
-import { ForgotPasswordForm } from './components/auth/ForgotPasswordForm';
-import ResetPassword from './pages/ResetPassword';
-import VerifyEmail from './pages/VerifyEmail';
-import AuthCallback from './pages/AuthCallback';
+import { ForgotPassword } from './pages/ForgotPassword';
+import { AuthCallback } from './components/auth/AuthCallback';
+import { ProtectedRoute } from './components/auth/ProtectedRoute';
 import UsersListPage from './pages/users';
 import UserDetailPage from './pages/users/[id]';
 import UserCreatePage from './pages/users/new';
@@ -27,15 +26,13 @@ import SubdomainDetailPage from './pages/subdomains/[id]';
 import SubdomainCreatePage from './pages/subdomains/new';
 import SubdomainEditPage from './pages/subdomains/[id]/edit';
-import AllowedEmailDomainsListPage from './pages/allowed-email-domains';
-import AllowedEmailDomainDetailPage from './pages/allowed-email-domains/[id]';
-import AllowedEmailDomainCreatePage from './pages/allowed-email-domains/new';
-import AllowedEmailDomainEditPage from './pages/allowed-email-domains/[id]/edit';
 import { useAuth } from './contexts/AuthContext';

 // PRISM:PROTECTED:START - Custom Imports
-// Add your custom page imports here:
-// import MyCustomPage from './pages/custom';
+import LandingPage from './pages/LandingPage';
+import Dashboard from './pages/Dashboard';
+import ResetPassword from './pages/ResetPassword';
+import VerifyEmail from './pages/VerifyEmail';
 // PRISM:PROTECTED:END

 /** App name and description for branding */
@@ -77,6 +74,8 @@
           {/* Navigation */}
           <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
+          {/* Admin-only: Users management */}
+          {user?.roles?.includes('admin') && (
           <NavLink
             to="/users"
             className={({ isActive }) =>
@@ -88,10 +87,13 @@             }
           >
             <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
-              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
+              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
             </svg>
             Users
           </NavLink>
+          )}
+          {/* Protected: API Keys (any authenticated user) */}
+          {isAuthenticated && (
           <NavLink
             to="/api-keys"
             className={({ isActive }) =>
@@ -103,10 +105,13 @@             }
           >
             <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
-              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
-            </svg>
-            APIKeys
-          </NavLink>
+              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
+            </svg>
+            API Keys
+          </NavLink>
+          )}
+          {/* Protected: Subdomains (any authenticated user) */}
+          {isAuthenticated && (
           <NavLink
             to="/subdomains"
             className={({ isActive }) =>
@@ -118,25 +123,46 @@             }
           >
             <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
-              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
+              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
             </svg>
             Subdomains
           </NavLink>
-          <NavLink
-            to="/allowed-email-domains"
-            className={({ isActive }) =>
-              `flex items-center gap-3 px-3 py-2 rounded-nordic text-sm font-medium transition-colors ${
-                isActive
-                  ? 'bg-nordic-100 text-nordic-900'
-                  : 'text-nordic-600 hover:bg-nordic-50 hover:text-nordic-900'
-              }`
-            }
-          >
-            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
-              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
-            </svg>
-            AllowedEmailDomains
-          </NavLink>
+          )}
+          {/* Unauthenticated: Login/Signup */}
+          {!isAuthenticated && (
+          <>
+          <NavLink
+            to="/login"
+            className={({ isActive }) =>
+              `flex items-center gap-3 px-3 py-2 rounded-nordic text-sm font-medium transition-colors ${
+                isActive
+                  ? 'bg-nordic-100 text-nordic-900'
+                  : 'text-nordic-600 hover:bg-nordic-50 hover:text-nordic-900'
+              }`
+            }
+          >
+            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
+              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
+            </svg>
+            Login
+          </NavLink>
+          <NavLink
+            to="/signup"
+            className={({ isActive }) =>
+              `flex items-center gap-3 px-3 py-2 rounded-nordic text-sm font-medium transition-colors ${
+                isActive
+                  ? 'bg-nordic-100 text-nordic-900'
+                  : 'text-nordic-600 hover:bg-nordic-50 hover:text-nordic-900'
+              }`
+            }
+          >
+            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
+              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
+            </svg>
+            Sign Up
+          </NavLink>
+          </>
+          )}
             {/* PRISM:PROTECTED:START - Custom Nav Links */}
             {/* Add your custom navigation links here */}
             {/* PRISM:PROTECTED:END */}
@@ -186,23 +212,10 @@   );
 }

-/** Home page with welcome message */
+/** Home page: landing for guests, dashboard for authenticated users */
 function HomePage(): ReactElement {
-  return (
-    <div className="page-container">
-      <div className="card p-8 text-center">
-        <div className="w-16 h-16 bg-surface-sunken rounded-full flex items-center justify-center mx-auto mb-4">
-          <svg className="w-8 h-8 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
-            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
-          </svg>
-        </div>
-        <h1 className="text-2xl font-semibold text-foreground mb-2">Welcome</h1>
-        <p className="text-muted max-w-md mx-auto">
-          Select an item from the sidebar to get started.
-        </p>
-      </div>
-    </div>
-  );
+  const { isAuthenticated } = useAuth();
+  return isAuthenticated ? <Dashboard /> : <LandingPage />;
 }

 /** Application router with all model routes */
@@ -211,31 +224,28 @@     element: <Layout />,
     children: [
       { path: '/', element: <HomePage /> },
-  { path: '/login', element: <Login /> },
-  { path: '/signup', element: <Signup /> },
-  { path: '/forgot-password', element: <ForgotPasswordForm /> },
-  { path: '/reset-password', element: <ResetPassword /> },
-  { path: '/verify-email', element: <VerifyEmail /> },
-  { path: '/auth/callback', element: <AuthCallback /> },
-  { path: '/users', element: <UsersListPage /> },
-  { path: '/users/:id', element: <UserDetailPage /> },
-  { path: '/users/new', element: <UserCreatePage /> },
-  { path: '/users/:id/edit', element: <UserEditPage /> },
-  { path: '/api-keys', element: <APIKeysListPage /> },
-  { path: '/api-keys/:id', element: <APIKeyDetailPage /> },
-  { path: '/api-keys/new', element: <APIKeyCreatePage /> },
-  { path: '/api-keys/:id/edit', element: <APIKeyEditPage /> },
-  { path: '/subdomains', element: <SubdomainsListPage /> },
-  { path: '/subdomains/:id', element: <SubdomainDetailPage /> },
-  { path: '/subdomains/new', element: <SubdomainCreatePage /> },
-  { path: '/subdomains/:id/edit', element: <SubdomainEditPage /> },
-  { path: '/allowed-email-domains', element: <AllowedEmailDomainsListPage /> },
-  { path: '/allowed-email-domains/:id', element: <AllowedEmailDomainDetailPage /> },
-  { path: '/allowed-email-domains/new', element: <AllowedEmailDomainCreatePage /> },
-  { path: '/allowed-email-domains/:id/edit', element: <AllowedEmailDomainEditPage /> },
+      // Public routes
+      { path: '/login', element: <Login /> },
+      { path: '/signup', element: <Signup /> },
+      { path: '/forgot-password', element: <ForgotPassword /> },
+      { path: '/auth/callback', element: <AuthCallback /> },
+      // Admin-only routes (Users management)
+      { path: '/users', element: <ProtectedRoute roles={['admin']}><UsersListPage /></ProtectedRoute> },
+      { path: '/users/:id', element: <ProtectedRoute roles={['admin']}><UserDetailPage /></ProtectedRoute> },
+      { path: '/users/new', element: <ProtectedRoute roles={['admin']}><UserCreatePage /></ProtectedRoute> },
+      { path: '/users/:id/edit', element: <ProtectedRoute roles={['admin']}><UserEditPage /></ProtectedRoute> },
+      // Protected routes (any authenticated user - users see their own)
+      { path: '/api-keys', element: <ProtectedRoute><APIKeysListPage /></ProtectedRoute> },
+      { path: '/api-keys/:id', element: <ProtectedRoute><APIKeyDetailPage /></ProtectedRoute> },
+      { path: '/api-keys/new', element: <ProtectedRoute><APIKeyCreatePage /></ProtectedRoute> },
+      { path: '/api-keys/:id/edit', element: <ProtectedRoute><APIKeyEditPage /></ProtectedRoute> },
+      { path: '/subdomains', element: <ProtectedRoute><SubdomainsListPage /></ProtectedRoute> },
+      { path: '/subdomains/:id', element: <ProtectedRoute><SubdomainDetailPage /></ProtectedRoute> },
+      { path: '/subdomains/new', element: <ProtectedRoute><SubdomainCreatePage /></ProtectedRoute> },
+      { path: '/subdomains/:id/edit', element: <ProtectedRoute><SubdomainEditPage /></ProtectedRoute> },
       // PRISM:PROTECTED:START - Custom Routes
-      // Add your custom routes here:
-      // { path: '/custom', element: <MyCustomPage /> },
+      { path: '/reset-password', element: <ResetPassword /> },
+      { path: '/verify-email', element: <VerifyEmail /> },
       // PRISM:PROTECTED:END
     ],
   },

```

</details>

### Actions

- Review your custom code to ensure it's still compatible
- Run `prism test` to verify functionality
- Run `prism review mark-reviewed packages/frontend/src/router.tsx` when done

---


## ⚠️ packages/backend/src/prisme_api/api/rest/subdomain.py

**Strategy**: generate_once
**Status**: Not Reviewed
**Changes**: +0 lines, -0 lines, ~560 lines
**Last Modified**: 2026-01-29T08:44:54.341319

### What Changed

<details>
<summary>Show Diff</summary>

```diff
--- generated+++ user@@ -1,26 +1,569 @@ """Custom REST API routes for Subdomain.

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
+import os
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
+limiter = Limiter(key_func=get_user_key, enabled="sqlite" not in os.environ.get("DATABASE_URL", ""))
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
**Last Modified**: 2026-01-29T08:44:54.336435

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
**Last Modified**: 2026-01-29T08:44:54.331084

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
**Changes**: +95 lines, -11 lines, ~57 lines
**Last Modified**: 2026-01-29T08:44:54.291424

### What Changed

<details>
<summary>Show Diff</summary>

```diff
--- generated+++ user@@ -1,7 +1,6 @@-"""Authentication routes — cookie-based JWT sessions.
-
-⚠️ AUTO-GENERATED BY PRISM (GENERATE_ONCE)
-Signup, login, email verification, password reset, MFA/TOTP, OAuth.
+"""Authentication routes — self-contained (no Authentik).
+
+Signup, login, email verification, password reset, MFA/TOTP, GitHub OAuth.
 """

 from __future__ import annotations
@@ -16,47 +15,87 @@ import httpx
 from fastapi import APIRouter, Cookie, Depends, HTTPException, Query, Response, status
 from fastapi.responses import RedirectResponse
+from pydantic import BaseModel, EmailStr
 from sqlalchemy import select
 from sqlalchemy.ext.asyncio import AsyncSession

-from prisme_api.auth.password_service import (
+from prisme_api.auth.config import auth_settings
+from prisme_api.auth.dependencies import CurrentActiveUser, create_session_jwt
+from prisme_api.auth.utils import (
     generate_token,
+    generate_totp_secret,
+    get_totp_uri,
     hash_password,
     validate_password_strength,
     verify_password,
+    verify_totp,
 )
-from prisme_api.auth.token_service import create_session_jwt
-from prisme_api.auth.config import auth_settings
 from prisme_api.database import get_db
-from prisme_api.middleware.auth import CurrentActiveUser
 from prisme_api.models.user import User
-from prisme_api.schemas.auth import (
-    LoginRequest,
-    LoginResponse,
-    UserResponse,
-    LoginMFARequest,
-    MFADisableRequest,
-    MFASetupResponse,
-    MFAVerifySetupRequest,
-    ResendVerificationRequest,
-    VerifyEmailRequest,
-    ForgotPasswordRequest,
-    ResetPasswordRequest,
-)
+from prisme_api.schemas.auth import UserResponse
 from prisme_api.services.email_service import (
-    send_verification_email,
     send_password_changed_notification,
     send_password_reset_email,
+    send_verification_email,
 )
-from prisme_api.auth.totp_service import (
-    generate_totp_secret,
-    get_totp_uri,
-    verify_totp,
-)

 logger = logging.getLogger(__name__)

 router = APIRouter(prefix="/auth", tags=["authentication"])
+
+
+# ── Request/Response schemas ────────────────────────────────────
+
+
+class SignupRequest(BaseModel):
+    email: EmailStr
+    username: str
+    password: str
+
+
+class LoginRequest(BaseModel):
+    email: EmailStr
+    password: str
+
+
+class LoginMFARequest(BaseModel):
+    email: EmailStr
+    code: str
+
+
+class VerifyEmailRequest(BaseModel):
+    token: str
+
+
+class ResendVerificationRequest(BaseModel):
+    email: EmailStr
+
+
+class ForgotPasswordRequest(BaseModel):
+    email: EmailStr
+
+
+class ResetPasswordRequest(BaseModel):
+    token: str
+    password: str
+
+
+class MFAVerifySetupRequest(BaseModel):
+    code: str
+
+
+class MFADisableRequest(BaseModel):
+    password: str
+
+
+class LoginResponse(BaseModel):
+    requires_mfa: bool = False
+    user: dict | None = None
+
+
+class MFASetupResponse(BaseModel):
+    totp_uri: str
+    secret: str


 # ── Helpers ─────────────────────────────────────────────────────
@@ -99,8 +138,10 @@ def _record_failed_login(user: User) -> None:
     """Increment failed attempts and lock if threshold reached."""
     user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
-    if user.failed_login_attempts >= 5:
-        user.locked_until = datetime.now(UTC) + timedelta(minutes=15)
+    if user.failed_login_attempts >= auth_settings.max_failed_login_attempts:
+        user.locked_until = datetime.now(UTC) + timedelta(
+            minutes=auth_settings.lockout_duration_minutes
+        )


 def _reset_failed_logins(user: User) -> None:
@@ -108,6 +149,22 @@     user.locked_until = None


+async def _validate_email_domain(db: AsyncSession, email: str) -> None:
+    """Check email domain against whitelist."""
+    try:
+        from prisme_api.services.allowed_email_domain import AllowedEmailDomainService
+
+        domain_service = AllowedEmailDomainService(db)
+        if not await domain_service.is_domain_allowed(email):
+            domain = email.split("@")[1] if "@" in email else "unknown"
+            raise HTTPException(
+                status_code=status.HTTP_403_FORBIDDEN,
+                detail=f"Email domain '{domain}' is not allowed for signup.",
+            )
+    except ImportError:
+        pass
+
+
 # ── Signup ──────────────────────────────────────────────────────


@@ -117,21 +174,23 @@     db: Annotated[AsyncSession, Depends(get_db)],
 ) -> dict[str, str]:
     """Create a new user account and send verification email."""
-    from prisme_api.schemas.auth import SignupRequest
-
+    # Validate password
     pw_error = validate_password_strength(body.password)
     if pw_error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=pw_error)

-    result = await db.execute(
-        select(User).where(User.email == body.email)
-    )
+    # Check if email already exists
+    result = await db.execute(select(User).where(User.email == body.email))
     if result.scalar_one_or_none():
         raise HTTPException(
             status_code=status.HTTP_409_CONFLICT,
             detail="An account with this email already exists.",
         )

+    # Validate email domain
+    await _validate_email_domain(db, body.email)
+
+    # Create user
     token = generate_token()
     user = User(
         email=body.email,
@@ -140,14 +199,16 @@         email_verified=False,
         email_verification_token=token,
         email_verification_token_expires_at=datetime.now(UTC)
-        + timedelta(hours=24),
+        + timedelta(hours=auth_settings.email_verification_token_hours),
         roles=["user"],
         is_active=True,
     )
     db.add(user)
     await db.commit()

+    # Send verification email
     send_verification_email(body.email, token)
+
     return {"message": "Account created. Please check your email to verify your address."}


@@ -161,9 +222,7 @@     db: Annotated[AsyncSession, Depends(get_db)],
 ) -> dict:
     """Verify email address and auto-login."""
-    result = await db.execute(
-        select(User).where(User.email_verification_token == body.token)
-    )
+    result = await db.execute(select(User).where(User.email_verification_token == body.token))
     user = result.scalar_one_or_none()

     if not user:
@@ -187,6 +246,7 @@     await db.commit()
     await db.refresh(user)

+    # Auto-login
     token = create_session_jwt(user)
     _set_session_cookie(response, token)

@@ -199,16 +259,14 @@     db: Annotated[AsyncSession, Depends(get_db)],
 ) -> dict[str, str]:
     """Resend verification email. Always returns 200 to prevent email enumeration."""
-    result = await db.execute(
-        select(User).where(User.email == body.email)
-    )
+    result = await db.execute(select(User).where(User.email == body.email))
     user = result.scalar_one_or_none()

     if user and not user.email_verified:
         token = generate_token()
         user.email_verification_token = token
         user.email_verification_token_expires_at = datetime.now(UTC) + timedelta(
-            hours=24
+            hours=auth_settings.email_verification_token_hours
         )
         await db.commit()
         send_verification_email(body.email, token)
@@ -225,10 +283,8 @@     response: Response,
     db: Annotated[AsyncSession, Depends(get_db)],
 ) -> LoginResponse:
-    """Login with email and password."""
-    result = await db.execute(
-        select(User).where(User.email == body.email)
-    )
+    """Login with email and password. Returns requires_mfa if MFA is enabled."""
+    result = await db.execute(select(User).where(User.email == body.email))
     user = result.scalar_one_or_none()

     if not user or not user.password_hash:
@@ -284,9 +340,7 @@     db: Annotated[AsyncSession, Depends(get_db)],
 ) -> LoginResponse:
     """Complete MFA login with TOTP code."""
-    result = await db.execute(
-        select(User).where(User.email == body.email)
-    )
+    result = await db.execute(select(User).where(User.email == body.email))
     user = result.scalar_one_or_none()

     if not user or not user.mfa_secret:
@@ -325,16 +379,14 @@     db: Annotated[AsyncSession, Depends(get_db)],
 ) -> dict[str, str]:
     """Send password reset email. Always returns 200 to prevent email enumeration."""
-    result = await db.execute(
-        select(User).where(User.email == body.email)
-    )
+    result = await db.execute(select(User).where(User.email == body.email))
     user = result.scalar_one_or_none()

     if user:
         token = generate_token()
         user.password_reset_token = token
         user.password_reset_token_expires_at = datetime.now(UTC) + timedelta(
-            hours=1
+            hours=auth_settings.password_reset_token_hours
         )
         await db.commit()
         send_password_reset_email(body.email, token)
@@ -353,9 +405,7 @@     if pw_error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=pw_error)

-    result = await db.execute(
-        select(User).where(User.password_reset_token == body.token)
-    )
+    result = await db.execute(select(User).where(User.password_reset_token == body.token))
     user = result.scalar_one_or_none()

     if not user:
@@ -364,9 +414,8 @@             detail="Invalid or expired reset token.",
         )

-    if (
-        user.password_reset_token_expires_at
-        and user.password_reset_token_expires_at < datetime.now(UTC)
+    if user.password_reset_token_expires_at and user.password_reset_token_expires_at < datetime.now(
+        UTC
     ):
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
@@ -382,6 +431,7 @@
     send_password_changed_notification(user.email)

+    # Auto-login
     token = create_session_jwt(user)
     _set_session_cookie(response, token)

@@ -398,6 +448,7 @@ ) -> MFASetupResponse:
     """Generate TOTP secret and URI for QR code. Requires authentication."""
     secret = generate_totp_secret()
+    # Store pending secret (not yet enabled)
     current_user.mfa_secret = secret
     await db.commit()

@@ -457,6 +508,7 @@ GITHUB_USER_API = "https://api.github.com/user"
 GITHUB_EMAILS_API = "https://api.github.com/user/emails"

+# In-memory state store (acceptable for single-instance; use Redis if scaling)
 _oauth_states: dict[str, float] = {}


@@ -510,6 +562,7 @@             url="/auth/callback?error=missing_params", status_code=status.HTTP_302_FOUND
         )

+    # Validate CSRF state
     if state not in _oauth_states:
         return RedirectResponse(
             url="/auth/callback?error=invalid_state", status_code=status.HTTP_302_FOUND
@@ -517,6 +570,7 @@     _oauth_states.pop(state, None)

     async with httpx.AsyncClient() as client:
+        # Exchange code for access token
         token_resp = await client.post(
             GITHUB_TOKEN_URL,
             data={
@@ -544,6 +598,7 @@
         auth_headers = {"Authorization": f"Bearer {access_token}"}

+        # Get user profile
         user_resp = await client.get(GITHUB_USER_API, headers=auth_headers)
         if user_resp.status_code != 200:
             return RedirectResponse(
@@ -552,6 +607,7 @@             )
         gh_user = user_resp.json()

+        # Get primary verified email
         email = gh_user.get("email")
         if not email:
             emails_resp = await client.get(GITHUB_EMAILS_API, headers=auth_headers)
@@ -566,9 +622,11 @@                 url="/auth/callback?error=no_email", status_code=status.HTTP_302_FOUND
             )

+    # Find or create user
     username = gh_user.get("login", email.split("@")[0])
     github_id = str(gh_user.get("id", ""))

+    # Try finding by github_id first
     result = await db.execute(select(User).where(User.github_id == github_id))
     user = result.scalar_one_or_none()

@@ -577,15 +635,19 @@         user = result.scalar_one_or_none()

     if user:
+        # Link github_id if not set
         if not user.github_id:
             user.github_id = github_id
             await db.commit()
     else:
+        # Validate email domain
+        await _validate_email_domain(db, email)
+
         user = User(
             email=email,
             username=username,
             github_id=github_id,
-            email_verified=True,
+            email_verified=True,  # GitHub emails are verified
             is_active=True,
             roles=["user"],
         )
@@ -593,9 +655,9 @@         await db.commit()
         await db.refresh(user)

-    jwt_token = create_session_jwt(user)
+    token = create_session_jwt(user)
     redirect = RedirectResponse(url="/auth/callback", status_code=status.HTTP_302_FOUND)
-    _set_session_cookie(redirect, jwt_token)
+    _set_session_cookie(redirect, token)
     return redirect


@@ -625,8 +687,6 @@     session_token: str | None = Cookie(None, alias=auth_settings.session_cookie_name),
 ) -> RedirectResponse:
     """Logout via GET: clear cookie and redirect to login."""
-    from fastapi.responses import RedirectResponse
-
     redirect = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
     redirect.delete_cookie(
         key=auth_settings.session_cookie_name,

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
**Last Modified**: 2026-01-29T08:44:54.247650

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
