# Authentication

All API requests require authentication using an API key.

## API Keys

API keys are bearer tokens prefixed with `prisme_live_sk_` (production) or `prisme_test_sk_` (testing).

### Using API Keys

Include your API key in the `Authorization` header:

```bash
curl -H "Authorization: Bearer prisme_live_sk_xxxxx" \
     https://api.prisme.dev/subdomains
```

### Key Security

!!! danger "Keep Your API Keys Secret"
    - Never commit API keys to version control
    - Never expose keys in client-side code
    - Use environment variables for storage
    - Rotate keys if compromised

## Rate Limiting

| Tier | Requests/minute | Subdomains |
|------|-----------------|------------|
| Free | 60 | 5 |
| Pro | 300 | 25 |
| Enterprise | Custom | Unlimited |

When rate limited, you'll receive a `429 Too Many Requests` response with headers:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1706270400
```

## Error Responses

All errors follow a consistent format:

```json
{
  "detail": "Invalid or missing API key"
}
```

### Common Error Codes

| Status | Description |
|--------|-------------|
| `401` | Missing or invalid API key |
| `403` | API key valid but insufficient permissions |
| `429` | Rate limit exceeded |
