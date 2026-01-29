# prisme-saas

A **subdomain-as-a-service platform** for managing `*.madewithpris.me` subdomains with wildcard DNS routing. Built with the [Prism framework](https://github.com/lassethomsen/prism).

## Skills

This project includes Claude Code skills for working with Prism:

- **`.claude/skills/prism-cli/`** — CLI commands, project structure, and workflow reference
- **`.claude/skills/generate-prism-spec/`** — Full spec API reference for writing `specs/models.py`

Use these when generating code, modifying the spec, or running CLI commands.

## Core Principle: Spec-First Development

1. **Define** models in `specs/models.py` (single source of truth)
2. **Generate** with `uv run prism generate`
3. **Customize** by extending generated base classes (never edit `_generated/` files)
4. **Regenerate** freely — customizations are preserved

## Project Context

- **Backend**: `packages/backend/src/prisme_api/` — Python 3.13, FastAPI, async SQLAlchemy, asyncpg
- **Frontend**: `packages/frontend/src/` — React 18, TypeScript, Vite, urql (GraphQL), Tailwind CSS
- **Spec**: `specs/models.py` — Model definitions
- **Config**: `prism.config.py`
- **Deploy**: `deploy/` — Terraform (Hetzner), Traefik, Authentik blueprints
- **Auth**: Authentik SSO (OIDC) + API keys + JWT
- **Email**: Resend API
- **Prism framework source**: `/home/lassethomsen/code/prism/`

### Models

| Model | Purpose |
|-------|---------|
| **User** | Accounts with email, MFA, authentik_id, roles (JSON), subdomain_limit, soft delete |
| **Subdomain** | `*.madewithpris.me` entries with DNS status lifecycle (reserved/active/suspended/released) |
| **APIKey** | Programmatic access tokens (SHA256 hashed, prefix, expiry) |
| **AllowedEmailDomain** | Signup email whitelist |

### Custom (non-generated) Code

- `services/hetzner_dns.py` — Hetzner DNS API for A record management
- `services/route_manager.py` — Traefik dynamic routing config
- `auth/` — OIDC, API key auth, webhooks, dependencies
- `middleware/` — Auth and API key middleware

## Critical Rules

**Never edit** (will be overwritten):
- `services/_generated/*.py`, `schemas/*.py`, `components/_generated/*.tsx`, `types/generated.ts`

**Safe to edit**:
- `services/<model>_service.py`, `components/<Model>Form.tsx`, `api/rest/*.py` (custom), `pages/*.tsx`

## Quick Commands

```bash
uv run prism generate              # Generate code from spec
uv run prism generate --dry-run    # Preview changes
uv run prism dev                   # Start dev servers
uv run prism dev --docker          # Start in Docker
uv run prism test                  # Run all tests
uv run prism db migrate            # Create/run migrations
uv run prism review list           # See override status
```

## Common Workflows

### Adding/Modifying Models

1. Edit `specs/models.py` (see `generate-prism-spec` skill for full API)
2. `uv run prism generate --dry-run` then `uv run prism generate`
3. `uv run prism db migrate -m "description"`

### Adding Custom Business Logic

Extend the generated service (NOT in `_generated/`):

```python
# services/subdomain_service.py
from ._generated.subdomain_service import SubdomainServiceBase

class SubdomainService(SubdomainServiceBase):
    async def create(self, data):
        # Custom logic before/after calling super()
        result = await super().create(data)
        return result
```

### Managing Overrides

```bash
uv run prism review list              # See all overrides
uv run prism review diff <file>       # See differences
uv run prism review mark-reviewed <file>  # Acknowledge
uv run prism review restore <file>    # Undo customizations
```

## Deployment

| Environment | Server | Volume |
|-------------|--------|--------|
| Staging | cx23 (1 vCPU, 2GB) | 10GB |
| Production | cpx21 (2 vCPU, 4GB) | 20GB |

## Required Environment Variables

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/prisme_api
PRISME_ADMIN_API_KEY=prisme_live_sk_...
HETZNER_DNS_API_TOKEN=...
HETZNER_DNS_ZONE_ID=...
SSL_EMAIL=admin@prisme.dev
DEBUG=true
```
