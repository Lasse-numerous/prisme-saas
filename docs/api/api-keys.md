# API Keys

Manage API keys for programmatic access to the MadeWithPris.me API.

## Overview

API keys allow CLI tools and scripts to authenticate without going through the SSO flow. Each user can create multiple API keys with different expiration dates.

!!! info "Owner-Based Access"
    Users can only see and manage their own API keys. Admins can see all API keys.

---

## List API Keys

```http
GET /api-keys
```

Returns a paginated list of your API keys.

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `page_size` | integer | 20 | Items per page (max 100) |
| `sort_by` | string | `created_at` | Field to sort by |
| `sort_order` | string | `desc` | Sort order (`asc` or `desc`) |

### Filters

| Parameter | Type | Description |
|-----------|------|-------------|
| `is_active` | boolean | Filter by active status |
| `name` | string | Filter by key name (exact match) |
| `name__ilike` | string | Filter by key name (case-insensitive pattern) |

### Response

```json
{
  "items": [
    {
      "id": 1,
      "name": "Production CLI",
      "key_prefix": "prisme_live_sk_abc",
      "is_active": true,
      "last_used_at": "2026-01-26T10:30:00Z",
      "expires_at": "2027-01-26T00:00:00Z",
      "created_at": "2026-01-15T00:00:00Z",
      "updated_at": "2026-01-26T10:30:00Z"
    },
    {
      "id": 2,
      "name": "CI/CD Pipeline",
      "key_prefix": "prisme_live_sk_def",
      "is_active": true,
      "last_used_at": null,
      "expires_at": null,
      "created_at": "2026-01-20T00:00:00Z",
      "updated_at": "2026-01-20T00:00:00Z"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

!!! note "Key Hash Not Exposed"
    The full API key and key hash are never returned in list or get responses for security.

---

## Get API Key

```http
GET /api-keys/{id}
```

Retrieve a specific API key by ID.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | API key ID |

### Response

```json
{
  "id": 1,
  "name": "Production CLI",
  "key_prefix": "prisme_live_sk_abc",
  "is_active": true,
  "last_used_at": "2026-01-26T10:30:00Z",
  "expires_at": "2027-01-26T00:00:00Z",
  "created_at": "2026-01-15T00:00:00Z",
  "updated_at": "2026-01-26T10:30:00Z"
}
```

### Errors

| Status | Description |
|--------|-------------|
| `404` | API key not found or not accessible |

---

## Create API Key

```http
POST /api-keys
```

Create a new API key.

### Request Body

```json
{
  "name": "My New Key",
  "expires_at": "2027-01-26T00:00:00Z"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Human-readable name for the key |
| `expires_at` | datetime | No | Expiration timestamp (null = never expires) |

### Response

```json
{
  "id": 3,
  "name": "My New Key",
  "key_prefix": "prisme_live_sk_xyz",
  "key": "prisme_live_sk_xyz123abc456def789...",
  "is_active": true,
  "last_used_at": null,
  "expires_at": "2027-01-26T00:00:00Z",
  "created_at": "2026-01-26T14:00:00Z",
  "updated_at": "2026-01-26T14:00:00Z"
}
```

!!! warning "Save Your Key"
    The full `key` value is **only returned once** at creation time. Store it securely immediately.

### Errors

| Status | Description |
|--------|-------------|
| `400` | Invalid request body |

---

## Update API Key

```http
PATCH /api-keys/{id}
```

Update an existing API key.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | API key ID |

### Request Body

All fields are optional:

```json
{
  "name": "Renamed Key",
  "is_active": false,
  "expires_at": "2028-01-01T00:00:00Z"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Update key name |
| `is_active` | boolean | Enable or disable the key |
| `expires_at` | datetime | Update expiration (null to remove) |

### Response

Returns the updated API key object.

### Errors

| Status | Description |
|--------|-------------|
| `404` | API key not found or not accessible |
| `400` | Invalid request body |

---

## Delete API Key

```http
DELETE /api-keys/{id}
```

Permanently delete an API key.

!!! warning "Irreversible"
    Deleting an API key is permanent. Any applications using this key will immediately lose access.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | API key ID |

### Response

```
HTTP 204 No Content
```

### Errors

| Status | Description |
|--------|-------------|
| `404` | API key not found or not accessible |

---

## Best Practices

### Key Rotation

Regularly rotate API keys to limit the impact of potential compromise:

1. Create a new API key
2. Update your applications to use the new key
3. Verify everything works
4. Delete the old key

### Naming Conventions

Use descriptive names that indicate the key's purpose:

- `Production CLI - MacBook Pro`
- `CI/CD Pipeline - GitHub Actions`
- `Development - Local Testing`

### Expiration

Set expiration dates for production keys:

- Production keys: 6-12 months
- CI/CD keys: Match your release cycle
- Development keys: Short-lived (30 days)

### Monitoring

Check `last_used_at` to identify unused keys that can be cleaned up.
