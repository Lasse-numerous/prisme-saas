# API Reference

The prisme.dev REST API allows you to manage subdomains programmatically.

## Base URL

```
https://api.prisme.dev
```

## Authentication

All API requests require a valid API key in the `Authorization` header:

```
Authorization: Bearer prisme_live_sk_xxxxx
```

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/subdomains` | List your subdomains |
| `POST` | `/subdomains/claim` | Claim a new subdomain |
| `POST` | `/subdomains/{name}/activate` | Activate with IP address |
| `GET` | `/subdomains/{name}/status` | Check DNS propagation |
| `POST` | `/subdomains/{name}/release` | Release a subdomain |

## Quick Links

- [Subdomains API](subdomains.md) - Full subdomain endpoint documentation
- [Authentication](authentication.md) - API key management
