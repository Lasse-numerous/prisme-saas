# Users API

Manage user accounts. All endpoints require **admin** role.

!!! note "Admin Only"
    User management endpoints are restricted to administrators. Regular users can view their own profile via `/auth/me`.

## List Users

```http
GET /users
```

Returns a paginated list of all users.

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
| `email` | string | Filter by email (exact match) |
| `email__ilike` | string | Filter by email (case-insensitive pattern) |
| `role` | string | Filter by role (`admin` or `user`) |
| `email_verified` | boolean | Filter by verification status |
| `mfa_enabled` | boolean | Filter by MFA status |

### Response

```json
{
  "items": [
    {
      "id": 1,
      "email": "admin@example.com",
      "role": "admin",
      "email_verified": true,
      "mfa_enabled": true,
      "subdomain_limit": 100,
      "authentik_id": "abc123",
      "created_at": "2026-01-01T00:00:00Z",
      "updated_at": "2026-01-26T12:00:00Z"
    },
    {
      "id": 2,
      "email": "user@example.com",
      "role": "user",
      "email_verified": true,
      "mfa_enabled": false,
      "subdomain_limit": 5,
      "authentik_id": "def456",
      "created_at": "2026-01-15T00:00:00Z",
      "updated_at": "2026-01-15T00:00:00Z"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

## Get User

```http
GET /users/{id}
```

Retrieve a specific user by ID.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | User ID |

### Response

```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "user",
  "email_verified": true,
  "mfa_enabled": false,
  "subdomain_limit": 5,
  "authentik_id": "abc123",
  "created_at": "2026-01-15T00:00:00Z",
  "updated_at": "2026-01-15T00:00:00Z"
}
```

### Errors

| Status | Description |
|--------|-------------|
| `404` | User not found |

---

## Create User

```http
POST /users
```

Create a new user account.

### Request Body

```json
{
  "email": "newuser@example.com",
  "role": "user",
  "subdomain_limit": 5,
  "authentik_id": "xyz789"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | User email address |
| `role` | string | No | Role (`admin` or `user`), defaults to `user` |
| `subdomain_limit` | integer | No | Max subdomains, defaults to 5 |
| `authentik_id` | string | No | Authentik user ID for SSO |

### Response

```json
{
  "id": 3,
  "email": "newuser@example.com",
  "role": "user",
  "email_verified": false,
  "mfa_enabled": false,
  "subdomain_limit": 5,
  "authentik_id": "xyz789",
  "created_at": "2026-01-26T14:00:00Z",
  "updated_at": "2026-01-26T14:00:00Z"
}
```

### Errors

| Status | Description |
|--------|-------------|
| `400` | Invalid request body |
| `409` | Email already exists |

---

## Update User

```http
PATCH /users/{id}
```

Update an existing user.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | User ID |

### Request Body

All fields are optional:

```json
{
  "role": "admin",
  "subdomain_limit": 25,
  "email_verified": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `role` | string | Role (`admin` or `user`) |
| `subdomain_limit` | integer | Max subdomains allowed |
| `email_verified` | boolean | Email verification status |
| `mfa_enabled` | boolean | MFA enabled status |

### Response

Returns the updated user object.

### Errors

| Status | Description |
|--------|-------------|
| `404` | User not found |
| `400` | Invalid request body |

---

## Delete User

```http
DELETE /users/{id}
```

Delete a user account.

!!! warning "Cascading Delete"
    Deleting a user will also delete all their subdomains and API keys.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | User ID |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hard` | boolean | false | Permanently delete (vs soft delete) |

### Response

**Soft Delete (default):**

Returns the user object with `deleted_at` timestamp set.

**Hard Delete:**

```
HTTP 204 No Content
```

### Errors

| Status | Description |
|--------|-------------|
| `404` | User not found |
