# Authentication

MadeWithPris.me supports two authentication methods:

1. **SSO Authentication** - For web-based access via Authentik
2. **API Key Authentication** - For programmatic/CLI access

## SSO Authentication (Authentik)

The web interface and API support Single Sign-On via [Authentik](https://goauthentik.io/), an open-source identity provider.

### Auth Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/auth/login` | Initiate OIDC login flow |
| `GET` | `/auth/callback` | OIDC callback handler |
| `GET` | `/auth/logout` | Logout (GET) |
| `POST` | `/auth/logout` | Logout (POST) |
| `GET` | `/auth/me` | Get current user info |
| `POST` | `/auth/refresh` | Refresh session |

### Login Flow

1. Redirect user to `/auth/login`
2. User authenticates with Authentik (supports MFA via TOTP or email)
3. Callback redirects to `/auth/callback` with authorization code
4. Session cookie is set for subsequent requests

### Get Current User

```http
GET /auth/me
```

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "user",
  "email_verified": true,
  "mfa_enabled": true,
  "subdomain_limit": 5,
  "created_at": "2026-01-26T12:00:00Z"
}
```

---

## API Key Authentication

API keys provide programmatic access for CLI tools and scripts.

### API Key Format

API keys are bearer tokens with the following prefixes:

- `prisme_live_sk_` - Production keys
- `prisme_test_sk_` - Testing keys

### Using API Keys

Include your API key in the `Authorization` header:

```bash
curl -H "Authorization: Bearer prisme_live_sk_xxxxx" \
     https://api.madewithpris.me/subdomains
```

### Creating API Keys

Create API keys via the API (requires authentication):

```http
POST /api-keys
```

```json
{
  "name": "My CLI Key",
  "expires_at": "2027-01-26T00:00:00Z"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "My CLI Key",
  "key_prefix": "prisme_live_sk_abc",
  "key": "prisme_live_sk_abc123...",
  "expires_at": "2027-01-26T00:00:00Z",
  "created_at": "2026-01-26T12:00:00Z"
}
```

!!! warning "Save Your Key"
    The full API key is only shown once at creation time. Store it securely.

### Key Security

!!! danger "Keep Your API Keys Secret"
    - Never commit API keys to version control
    - Never expose keys in client-side code
    - Use environment variables for storage
    - Rotate keys if compromised
    - Set expiration dates for production keys

---

## Access Control

MadeWithPris.me uses role-based access control with owner-based filtering.

### Roles

| Role | Permissions |
|------|-------------|
| `admin` | Full access to all resources |
| `user` | Access to own resources only |

### Owner-Based Access

- **Subdomains**: Users can only see and manage their own subdomains
- **API Keys**: Users can only see and manage their own API keys
- **Users**: Only admins can access user management endpoints

---

## Error Responses

All errors follow a consistent format:

```json
{
  "detail": "Error message here"
}
```

### Common Error Codes

| Status | Description |
|--------|-------------|
| `401` | Missing or invalid authentication |
| `403` | Valid auth but insufficient permissions |
| `404` | Resource not found or not accessible |

### Authentication Errors

**Missing Authentication:**

```json
{
  "detail": "Not authenticated"
}
```

**Invalid API Key:**

```json
{
  "detail": "Invalid or expired API key"
}
```

**Insufficient Permissions:**

```json
{
  "detail": "You do not have permission to access this resource"
}
```
