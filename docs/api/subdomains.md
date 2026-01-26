# Subdomains API

Manage your prisme.dev subdomains.

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
- Cannot be a reserved name

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

Activate a subdomain by setting its IP address. Creates a DNS A record.

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
| `404` | Subdomain not found |

---

## Check Status

```http
GET /subdomains/{name}/status
```

Check DNS propagation status for a subdomain.

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

---

## Release Subdomain

```http
POST /subdomains/{name}/release
```

Release a subdomain, making it available for others.

!!! warning
    This action is irreversible. The DNS record will be deleted.

### Response

```json
{
  "message": "Subdomain released successfully"
}
```

### Errors

| Status | Description |
|--------|-------------|
| `404` | Subdomain not found |
