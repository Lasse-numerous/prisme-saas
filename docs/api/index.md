# API Reference

The MadeWithPris.me REST API allows you to manage subdomains, users, and API keys programmatically.

## Base URL

```
https://api.madewithpris.me
```

## Authentication

All API requests require authentication via either:

- **Session cookie** (from SSO login)
- **API key** in the `Authorization` header

```
Authorization: Bearer prisme_live_sk_xxxxx
```

See [Authentication](authentication.md) for details.

---

## Endpoints Overview

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/auth/login` | Initiate SSO login |
| `GET` | `/auth/callback` | SSO callback handler |
| `GET` | `/auth/logout` | Logout (GET) |
| `POST` | `/auth/logout` | Logout (POST) |
| `GET` | `/auth/me` | Get current user |
| `POST` | `/auth/refresh` | Refresh session |

### Subdomains

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/subdomains` | List your subdomains |
| `GET` | `/subdomains/{id}` | Get subdomain by ID |
| `POST` | `/subdomains/claim` | Claim a new subdomain |
| `POST` | `/subdomains/{name}/activate` | Activate with IP address |
| `GET` | `/subdomains/{name}/status` | Check DNS propagation |
| `POST` | `/subdomains/{name}/release` | Release a subdomain |
| `DELETE` | `/subdomains/{id}` | Delete a subdomain |

### API Keys

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api-keys` | List your API keys |
| `GET` | `/api-keys/{id}` | Get API key by ID |
| `POST` | `/api-keys` | Create new API key |
| `PATCH` | `/api-keys/{id}` | Update API key |
| `DELETE` | `/api-keys/{id}` | Delete API key |

### Users (Admin Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/users` | List all users |
| `GET` | `/users/{id}` | Get user by ID |
| `POST` | `/users` | Create user |
| `PATCH` | `/users/{id}` | Update user |
| `DELETE` | `/users/{id}` | Delete user |

---

## Common Patterns

### Pagination

All list endpoints support pagination:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number (1-indexed) |
| `page_size` | integer | 20 | Items per page (max 100) |

**Response Format:**

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```

### Sorting

All list endpoints support sorting:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sort_by` | string | `created_at` | Field to sort by |
| `sort_order` | string | `desc` | `asc` or `desc` |

### Filtering

List endpoints support field-specific filters with operators:

| Suffix | Operator | Example |
|--------|----------|---------|
| (none) | Equals | `status=active` |
| `__ne` | Not equals | `status__ne=released` |
| `__gt` | Greater than | `created_at__gt=2026-01-01` |
| `__gte` | Greater or equal | `subdomain_limit__gte=5` |
| `__lt` | Less than | `expires_at__lt=2027-01-01` |
| `__lte` | Less or equal | `id__lte=100` |
| `__like` | Pattern match | `name__like=%app%` |
| `__ilike` | Case-insensitive pattern | `email__ilike=%@example.com` |
| `__in` | In list | `status__in=active,reserved` |

---

## Error Handling

All errors return a consistent JSON format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

| Status | Description |
|--------|-------------|
| `200` | Success |
| `201` | Created |
| `204` | No Content (successful delete) |
| `400` | Bad Request - Invalid input |
| `401` | Unauthorized - Missing/invalid auth |
| `403` | Forbidden - Insufficient permissions |
| `404` | Not Found |
| `409` | Conflict - Resource already exists |
| `502` | Bad Gateway - External service error (e.g., DNS) |

---

## Quick Links

- [Authentication](authentication.md) - SSO and API key authentication
- [Subdomains API](subdomains.md) - Manage subdomains
- [API Keys](api-keys.md) - Manage API keys
- [Users API](users.md) - User management (admin)
