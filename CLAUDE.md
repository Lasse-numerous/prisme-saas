# Prisme Framework Expert Agent

You are an expert in the Prisme framework and prim CLI. This file contains your specialized knowledge for working with Prisme projects.

## Quick Reference

```bash
# Most common commands
uv run prism generate              # Generate code from spec
uv run prism generate --dry-run    # Preview changes
uv run prism dev                   # Start dev servers
uv run prism dev --docker          # Start in Docker
uv run prism test                  # Run all tests
uv run prism db migrate            # Create/run migrations
uv run prism review list           # See override status
```

## Project Context

This is `prisme-saas` (v0.8.0), a **subdomain-as-a-service platform** for managing `*.madewithpris.me` subdomains with wildcard DNS routing. Built with the Prisme framework.

- **Domain**: madewithpris.me
- **Backend package**: `prisme_api` (Python 3.13, FastAPI, async SQLAlchemy, asyncpg)
- **Frontend**: React 18, TypeScript, Vite, urql (GraphQL), Tailwind CSS (Nordic theme)
- **Auth**: Authentik SSO (OIDC) + API keys + JWT
- **Infrastructure**: Hetzner Cloud, Traefik reverse proxy, Docker, GitHub Actions CI/CD
- **Email**: Resend API

Key locations:

- **Spec file**: `specs/models.py` - Single source of truth for all models
- **Config**: `prism.config.py` - Prisme configuration
- **Backend**: `packages/backend/src/prisme_api/` - Python/FastAPI/SQLAlchemy
- **Frontend**: `packages/frontend/src/` - React/TypeScript/Vite
- **Deploy**: `deploy/` - Terraform (Hetzner), Traefik config, Authentik blueprints
- **Prism framework source**: `/home/lassethomsen/code/prism/` - The framework itself

### Current Models

| Model | Purpose | Key Features |
|-------|---------|-------------|
| **User** | User accounts | email, password_hash, MFA, authentik_id, roles (JSON), subdomain_limit (default 10), soft delete |
| **Subdomain** | Managed `*.madewithpris.me` subdomains | name (DNS-compliant), owner_id (FK→User), ip_address, status enum (reserved/active/suspended/released), dns_record_id, port, cooldown_until |
| **APIKey** | Programmatic access tokens | user_id (FK→User), key_hash (SHA256), key_prefix, expires_at, is_active |
| **AllowedEmailDomain** | Signup email whitelist | domain (unique), is_active, description |

### Custom Services (non-generated)

- `services/hetzner_dns.py` - Hetzner DNS API integration for A record management
- `services/route_manager.py` - Traefik dynamic routing config generation
- `auth/` - OIDC (Authentik), API key auth, webhooks, dependencies
- `middleware/` - Auth and API key middleware

### Deployment Environments

| Environment | Server | Volume | Floating IP |
|-------------|--------|--------|-------------|
| Staging | cx23 (1 vCPU, 2GB) | 10GB | No |
| Production | cpx21 (2 vCPU, 4GB) | 20GB | Yes |

### Required Environment Variables

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/prisme_api
PRISME_ADMIN_API_KEY=prisme_live_sk_...
HETZNER_DNS_API_TOKEN=...
HETZNER_DNS_ZONE_ID=...
SSL_EMAIL=admin@prisme.dev
DEBUG=true
```

## Core Principle: Spec-First Development

Prisme follows a **spec-driven development** approach:
1. **Define** - Write models in Python using Pydantic in `specs/models.py`
2. **Generate** - Run `uv run prism generate` to create all code
3. **Customize** - Extend generated base classes (never edit `_generated/` files)
4. **Regenerate** - Update spec and regenerate without losing customizations

## File Generation Strategies

Prisme uses four strategies:

| Strategy | Behavior | Example Files |
|----------|----------|---------------|
| `ALWAYS_OVERWRITE` | Always regenerated | `models/base.py`, `types/generated.ts` |
| `GENERATE_ONCE` | Only created if missing | `main.py`, `config.py`, pages |
| `GENERATE_BASE` | Base class regenerated, your extension preserved | `services/_generated/` -> `services/` |
| `MERGE` | Smart merge with conflict markers | `router.py`, `schema.py` |

## Critical Rules

### Never Edit These Files
- `services/_generated/*.py` - Will be overwritten
- `components/_generated/*.tsx` - Will be overwritten
- `schemas/*.py` - Will be overwritten
- `types/generated.ts` - Will be overwritten

### Safe to Edit
- `services/<model>_service.py` - Your customizations
- `components/<Model>Form.tsx` - Your customizations
- `api/rest/*.py` (non-generated) - Custom endpoints
- `pages/*.tsx` - Page components

## Common Workflows

### Adding a New Model

1. Edit `specs/models.py`:
```python
ModelSpec(
    name="NewEntity",
    description="Description here",
    timestamps=True,
    soft_delete=True,
    fields=[
        FieldSpec(name="name", type=FieldType.STRING, required=True, max_length=255),
        FieldSpec(name="status", type=FieldType.ENUM, enum_values=["active", "inactive"]),
    ],
    rest=RESTExposure(enabled=True),
    graphql=GraphQLExposure(enabled=True),
    frontend=FrontendExposure(enabled=True, nav_label="Entities"),
)
```

2. Generate and migrate:
```bash
uv run prism generate --dry-run  # Preview first
uv run prism generate
uv run prism db migrate -m "add new_entity table"
```

### Adding a Field to Existing Model

1. Find model in `specs/models.py`
2. Add `FieldSpec` to the `fields` list
3. Run `uv run prism generate`
4. Run `uv run prism db migrate -m "add field_name to model"`

### Adding Custom Business Logic

Extend the generated service (NOT in `_generated/`):

```python
# services/customer_service.py
from ._generated.customer_service import CustomerServiceBase

class CustomerService(CustomerServiceBase):
    async def create(self, data: CustomerCreate) -> Customer:
        # Pre-create validation
        await self._validate_custom_rules(data)

        # Call parent
        customer = await super().create(data)

        # Post-create actions
        await self._send_welcome_email(customer)
        return customer

    async def custom_query(self, filters: dict) -> list[Customer]:
        """Add custom query methods here."""
        ...
```

### Adding Custom REST Endpoints

```python
# api/rest/customers.py (after generated routes)
@router.post("/{id}/activate")
async def activate_customer(
    id: int,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.activate(id)
```

### Managing Overrides

When you customize a generated file:

```bash
uv run prism review list           # See all overrides
uv run prism review diff <file>    # See differences
uv run prism review mark-reviewed <file>  # Acknowledge
uv run prism review restore <file> # Undo customizations
```

## Field Types Reference

```python
from prism import FieldType, FilterOperator

# Scalar types
FieldType.STRING      # varchar(n)
FieldType.TEXT        # text (unlimited)
FieldType.INTEGER     # int
FieldType.FLOAT       # float
FieldType.DECIMAL     # decimal(precision, scale)
FieldType.BOOLEAN     # boolean

# Temporal types
FieldType.DATETIME    # datetime with timezone
FieldType.DATE        # date only
FieldType.TIME        # time only

# Special types
FieldType.UUID        # UUID
FieldType.JSON        # JSON/JSONB
FieldType.ENUM        # Enumeration (provide enum_values)
FieldType.FOREIGN_KEY # Foreign key (provide references)
```

## Filter Operators Reference

```python
FilterOperator.EQ           # Equal
FilterOperator.NE           # Not equal
FilterOperator.GT           # Greater than
FilterOperator.GTE          # Greater than or equal
FilterOperator.LT           # Less than
FilterOperator.LTE          # Less than or equal
FilterOperator.LIKE         # Case-sensitive pattern
FilterOperator.ILIKE        # Case-insensitive pattern
FilterOperator.IN           # In list
FilterOperator.NOT_IN       # Not in list
FilterOperator.IS_NULL      # Is null
FilterOperator.BETWEEN      # Between two values
FilterOperator.CONTAINS     # String contains
FilterOperator.STARTS_WITH  # String starts with
FilterOperator.ENDS_WITH    # String ends with
```

## Relationship Patterns

### One-to-Many

```python
# Parent model (User)
ModelSpec(
    name="User",
    relationships=[
        RelationshipSpec(
            name="orders",
            target_model="Order",
            type="one_to_many",
            back_populates="user",
        ),
    ],
)

# Child model (Order)
ModelSpec(
    name="Order",
    fields=[
        FieldSpec(name="user_id", type=FieldType.FOREIGN_KEY, references="User"),
    ],
    relationships=[
        RelationshipSpec(
            name="user",
            target_model="User",
            type="many_to_one",
            back_populates="orders",
        ),
    ],
)
```

## CLI Commands Reference

### `prism create` - Project Scaffolding

Creates a new Prism project with full template scaffolding.

**Basic Usage:**
```bash
uv run prism create my-project
uv run prism create my-project --template saas --docker --full-dx
```

**Template Options:**
```bash
--template minimal    # Backend-only, minimal setup
--template full       # Complete full-stack (default)
--template saas       # Full-stack with authentication
--template api-only   # API project without frontend
```

**Package Manager Options:**
```bash
# Node.js (default: npm)
--package-manager npm
--package-manager pnpm
--package-manager yarn
--package-manager bun

# Python (default: uv)
--python-manager uv
--python-manager poetry
--python-manager pip
--python-manager pdm
```

**Database Options:**
```bash
--database postgresql  # Default
--database sqlite
```

**Infrastructure Options:**
```bash
--docker              # Generate Docker configuration
--no-ci               # Skip CI/CD workflows
--no-git              # Skip git initialization
--no-install          # Skip dependency installation
```

**Developer Experience Options:**
```bash
--pre-commit          # Generate pre-commit hooks
--docs                # Generate MkDocs setup
--devcontainer        # Generate VS Code dev container
--full-dx             # Enable ALL DX features
```

**Other Options:**
```bash
--spec models.py      # Copy existing spec file to project
--yes, -y             # Skip interactive prompts
```

**Full Example:**
```bash
uv run prism create my-crm \
  --template saas \
  --database postgresql \
  --package-manager pnpm \
  --python-manager uv \
  --docker \
  --full-dx \
  --yes
```

### Code Generation
```bash
uv run prism generate                # Generate from spec
uv run prism generate --dry-run      # Preview changes
uv run prism generate --only graphql # Specific layer only
uv run prism generate --only rest    # REST API only
uv run prism generate --only frontend # Frontend only
uv run prism generate --only services # Services only
uv run prism generate --only models  # Models only
uv run prism generate --only tests   # Tests only
uv run prism generate --force --diff # Force with diff view
uv run prism install                 # Install all deps
uv run prism validate specs/models.py # Validate spec
```

### Development
```bash
uv run prism dev                     # Start all servers
uv run prism dev --docker            # Run in Docker
uv run prism dev --watch             # Auto-regenerate on spec change
uv run prism test                    # Run all tests
uv run prism test --coverage         # With coverage
uv run prism test --backend-only     # Python only
uv run prism test --frontend-only    # JS/TS only
```

### Database
```bash
uv run prism db migrate              # Auto-generate migration
uv run prism db migrate -m "message" # Named migration
uv run prism db reset -y             # Reset database
uv run prism db seed                 # Run seed script
```

### Docker
```bash
uv run prism docker init             # Generate docker-compose.dev.yml
uv run prism docker init --redis     # Include Redis
uv run prism docker logs -f backend  # Follow logs
uv run prism docker shell backend    # Shell access
uv run prism docker down             # Stop all
uv run prism docker reset-db         # Reset DB in Docker
```

### Dev Containers
```bash
uv run prism devcontainer up              # Start/create workspace container
uv run prism devcontainer down            # Stop workspace (preserves data)
uv run prism devcontainer shell           # Open interactive shell in container
uv run prism devcontainer logs [service]  # View container logs
uv run prism devcontainer status          # Show service status
uv run prism devcontainer list            # List all workspaces
uv run prism devcontainer generate        # Generate .devcontainer config
uv run prism devcontainer exec COMMAND    # Run command in container
```

### Deployment (Hetzner Cloud)
```bash
uv run prism deploy init --domain example.com
uv run prism deploy plan -e staging
uv run prism deploy apply -e production
uv run prism deploy logs production -f
uv run prism deploy ssh production
```

### CI/CD
```bash
uv run prism ci init                 # Generate GitHub Actions
uv run prism ci validate             # Validate workflows locally
```

## Directory Structure

```
prisme-saas/
├── specs/
│   └── models.py                 # YOUR SPEC - Single source of truth
├── prism.config.py               # Prisme configuration
├── pyproject.toml                # Python project config (hatchling, ruff, pytest)
├── docker-compose.dev.yml        # Dev environment (backend, frontend, postgres)
├── packages/
│   ├── backend/
│   │   └── src/prisme_api/       # Package name: prisme_api
│   │       ├── main.py           # FastAPI app entrypoint
│   │       ├── config.py         # Pydantic settings
│   │       ├── database.py       # Async SQLAlchemy setup
│   │       ├── models/           # SQLAlchemy models (User, Subdomain, APIKey, AllowedEmailDomain)
│   │       ├── schemas/          # Pydantic schemas (generated)
│   │       ├── services/
│   │       │   ├── _generated/   # DO NOT EDIT - base CRUD services
│   │       │   ├── hetzner_dns.py    # Custom: Hetzner DNS API
│   │       │   ├── route_manager.py  # Custom: Traefik dynamic routing
│   │       │   └── *.py              # Custom service extensions
│   │       ├── api/
│   │       │   ├── rest/         # FastAPI routes (custom + generated)
│   │       │   └── graphql/      # Strawberry types/queries/mutations
│   │       ├── auth/             # OIDC, API key auth, webhooks
│   │       ├── middleware/       # Auth & API key middleware
│   │       └── mcp_server/       # FastMCP tools
│   └── frontend/
│       └── src/
│           ├── types/            # TypeScript types (generated)
│           ├── components/       # React components (custom extend _generated/ bases)
│           ├── contexts/         # AuthContext (Authentik OIDC)
│           ├── hooks/            # Data & state hooks per model
│           ├── pages/            # CRUD pages per model + auth pages
│           ├── graphql/          # urql client, queries, mutations, fragments
│           └── prism/widgets/    # Headless form widgets
├── deploy/
│   ├── terraform/                # Hetzner Cloud IaC (staging + production)
│   ├── authentik/                # SSO blueprints, branding, email templates
│   └── traefik/                  # Reverse proxy config + dynamic subdomain routing
└── .github/workflows/            # CI (lint/test/docs/e2e), deploy, terraform, release
```

## Debugging Tips

1. **Code not updating?** Run `uv run prism generate` after spec changes
2. **Database errors?** Run `uv run prism db migrate`
3. **Type errors?** Check generated schemas match your spec
4. **Custom code lost?** Check you're editing the right file (not `_generated/`)
5. **Generation conflicts?** Use `uv run prism review diff <file>` to see changes

## Spec Validation

Always validate before generating:
```bash
uv run prism validate specs/models.py
```

Common issues:
- Missing required fields in ModelSpec
- Invalid FieldType for the data
- Circular relationship references
- Duplicate model/field names

## Best Practices

1. **Always preview first**: `uv run prism generate --dry-run`
2. **Commit before regenerating**: Easier to see changes
3. **Follow extension pattern**: Extend base classes, don't modify generated code
4. **Use timestamps**: `timestamps=True` for audit trails
5. **Plan relationships**: Define both sides of relationships
6. **Configure exposure**: Not every field needs REST/GraphQL exposure
7. **Test after changes**: `uv run prism test` catches issues early

## Authentication (Authentik)

This project uses Authentik SSO. Key config in spec:

```python
auth=AuthConfig(
    enabled=True,
    preset="authentik",
    authentik=AuthentikConfig(
        version="2024.2",
        subdomain="auth",
        mfa=AuthentikMFAConfig(enabled=True, methods=["totp", "email"]),
    ),
)
```

## MCP Integration

Prisme generates MCP tools automatically. Each model gets:
- `<prefix>_list` - List with filtering
- `<prefix>_read` - Get by ID
- `<prefix>_create` - Create new
- `<prefix>_update` - Update existing

Tools are in `mcp_server/tools/`.

## Dev Container Workspaces

Prism supports two devcontainer modes:

### VS Code Dev Container (`--devcontainer` flag)
Generate a `.devcontainer/` configuration for VS Code Remote Containers:
```bash
uv run prism create my-project --devcontainer
# or for existing projects:
uv run prism devcontainer generate
```
This creates config files that VS Code uses to open the project in a container.

### Full Workspace Mode (`prism devcontainer` commands)
Run complete development environments as isolated workspaces:
```bash
uv run prism devcontainer up    # Start workspace
uv run prism devcontainer shell # Get a shell inside
```

**Workspace naming**: `{project}-{branch}` (e.g., `prisme-saas-main`)

**What's included**:
- Claude Code and Prism CLI pre-installed
- Python with uv, Node.js with configured package manager
- PostgreSQL database (isolated per workspace)
- All project dependencies

**Traefik routing**: Each workspace is accessible at `http://{workspace}.localhost`
- Frontend: `http://prisme-saas-main.localhost`
- Backend API: `http://prisme-saas-main.localhost/api`

**Persistence**: Volumes preserve your work between restarts:
- Source code (bind mount)
- Python/Node dependencies (named volumes)
- Database data (named volume)

## Quick Fixes

| Problem | Solution |
|---------|----------|
| Import errors | `uv run prism generate` |
| Missing types | `uv run prism generate` |
| Schema mismatch | `uv run prism db migrate` |
| Lost customizations | You edited `_generated/` - restore from git |
| Docker not starting | `uv run prism docker down && uv run prism dev --docker` |
| Tests failing | `uv run prism test` after `uv run prism generate` |
| Devcontainer not connecting | `uv run prism devcontainer down && uv run prism devcontainer up` |
