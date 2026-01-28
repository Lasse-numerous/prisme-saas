# Subdomains API

Manage your madewithpris.me subdomains.

!!! info "Owner-Based Access"
    Users can only see and manage their own subdomains. Admins can see all subdomains.

## List Subdomains

```http
GET /subdomains
```

Returns a paginated list of your subdomains.

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
| `status` | string | Filter by status (`reserved`, `active`, `suspended`, `released`) |
| `status__in` | string | Filter by multiple statuses (comma-separated) |
| `name` | string | Filter by exact name |
| `name__ilike` | string | Filter by name pattern (case-insensitive) |
| `ip_address` | string | Filter by IP address |

### Response

```json
{
  "items": [
    {
      "id": 1,
      "name": "myapp",
      "ip_address": "1.2.3.4",
      "status": "active",
      "dns_record_id": "abc123",
      "created_at": "2026-01-26T12:00:00Z",
      "updated_at": "2026-01-26T12:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

## Get Subdomain

```http
GET /subdomains/{id}
```

Retrieve a specific subdomain by ID.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Subdomain ID |

### Response

```json
{
  "id": 1,
  "name": "myapp",
  "ip_address": "1.2.3.4",
  "status": "active",
  "dns_record_id": "abc123",
  "created_at": "2026-01-26T12:00:00Z",
  "updated_at": "2026-01-26T12:00:00Z"
}
```

### Errors

| Status | Description |
|--------|-------------|
| `404` | Subdomain not found or not accessible |

---

## Claim Subdomain

```http
POST /subdomains/claim
```

Reserve a new subdomain.

### Request Body

```json
{
  "name": "myapp"
}
```

### Validation

- `name` must be 3-63 characters
- Must start and end with alphanumeric characters
- Can contain lowercase letters, numbers, and hyphens
- Cannot be a reserved name (see [Reserved Names](#reserved-names))

### Response

```json
{
  "id": 1,
  "name": "myapp",
  "ip_address": null,
  "status": "reserved",
  "dns_record_id": null,
  "created_at": "2026-01-26T12:00:00Z",
  "updated_at": "2026-01-26T12:00:00Z"
}
```

### Errors

| Status | Description |
|--------|-------------|
| `400` | Invalid subdomain name |
| `409` | Subdomain already taken |

---

## Activate Subdomain

```http
POST /subdomains/{name}/activate
```

Activate a subdomain by setting its IP address. Configures our proxy to route traffic to your server.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Subdomain name |

### Request Body

```json
{
  "ip_address": "1.2.3.4"
}
```

### IP Address Validation

- Must be a valid IPv4 address
- Private/reserved ranges are allowed (for testing)

### Response

```json
{
  "id": 1,
  "name": "myapp",
  "ip_address": "1.2.3.4",
  "status": "active",
  "dns_record_id": "abc123",
  "created_at": "2026-01-26T12:00:00Z",
  "updated_at": "2026-01-26T12:30:00Z"
}
```

### Errors

| Status | Description |
|--------|-------------|
| `400` | Invalid IP address |
| `403` | Subdomain is suspended |
| `404` | Subdomain not found or not owned by you |
| `502` | DNS service error |

---

## Check Status

```http
GET /subdomains/{name}/status
```

Check DNS propagation status for a subdomain.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Subdomain name |

### Response

```json
{
  "name": "myapp",
  "status": "active",
  "ip_address": "1.2.3.4",
  "dns_propagated": true,
  "propagation_details": {
    "google": true,
    "cloudflare": true,
    "quad9": true
  }
}
```

### Propagation Details

DNS propagation is checked against multiple resolvers:

| Resolver | IP |
|----------|-----|
| Google | 8.8.8.8 |
| Cloudflare | 1.1.1.1 |
| Quad9 | 9.9.9.9 |

`dns_propagated` is `true` when all resolvers return the expected IP address.

### Errors

| Status | Description |
|--------|-------------|
| `404` | Subdomain not found or not accessible |

---

## Release Subdomain

```http
POST /subdomains/{name}/release
```

Release a subdomain, making it available for others to claim.

!!! warning "Irreversible"
    This action is irreversible. The proxy route will be removed and the subdomain name becomes available for anyone to claim.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Subdomain name |

### Response

```json
{
  "message": "Subdomain released successfully"
}
```

### Errors

| Status | Description |
|--------|-------------|
| `404` | Subdomain not found or not accessible |
| `502` | DNS deletion failed |

---

## Delete Subdomain

```http
DELETE /subdomains/{id}
```

Delete a subdomain by ID.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Subdomain ID |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hard` | boolean | false | Permanently delete vs soft delete |

### Response

**Soft Delete (default):**

Returns the subdomain with `deleted_at` timestamp set.

**Hard Delete:**

```
HTTP 204 No Content
```

### Errors

| Status | Description |
|--------|-------------|
| `404` | Subdomain not found or not accessible |

---

## Subdomain Statuses

| Status | Description |
|--------|-------------|
| `reserved` | Claimed but not activated (no IP set) |
| `active` | Activated with proxy route configured |
| `suspended` | Temporarily disabled by admin |
| `released` | Deleted/released |

---

## Reserved Names

The following subdomain names are reserved and cannot be claimed:

!!! info "Reserved Names"
    `www`, `api`, `app`, `admin`, `mail`, `smtp`, `pop`, `imap`, `ftp`, `ssh`, `dns`, `ns`, `ns1`, `ns2`, `ns3`, `mx`, `mx1`, `mx2`, `webmail`, `cpanel`, `whm`, `dashboard`, `portal`, `login`, `auth`, `oauth`, `sso`, `cdn`, `static`, `assets`, `media`, `img`, `images`, `video`, `docs`, `doc`, `help`, `support`, `status`, `blog`, `news`, `shop`, `store`, `pay`, `billing`, `invoice`, `git`, `gitlab`, `github`, `bitbucket`, `test`, `staging`, `dev`, `demo`, `beta`, `alpha`, `internal`
