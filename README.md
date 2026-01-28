# MadeWithPris.me

**Managed subdomain service for Prism projects** - Get `https://yourapp.madewithpris.me` in minutes.

## Overview

MadeWithPris.me provides managed `*.madewithpris.me` subdomains with automatic HTTPS for Prism projects deployed to Hetzner. You bring your own server, we handle the DNS.

## Quick Start

```bash
# Install dependencies
uv sync

# Start database
docker-compose -f docker-compose.dev.yml up -d db

# Generate code from spec
prism generate

# Run the API
uvicorn prisme_api.main:app --reload
```

## Development

```bash
# Run with Docker (recommended)
docker-compose -f docker-compose.dev.yml up

# Access at http://madewithpris.me.localhost (requires Traefik proxy)
# Or directly at http://localhost:8000
```

## Development with Devcontainer

```bash
prism devcontainer up      # Start the devcontainer environment
prism devcontainer shell   # Open a shell inside the container
```

This provides a consistent development environment with all dependencies pre-configured.

## API Documentation

- OpenAPI docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Production

- **Domain**: madewithpris.me (GoDaddy)
- **API**: api.madewithpris.me
- **Subdomains**: *.madewithpris.me

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│  prism CLI      │────▶│ MadeWithPris.me  │────▶│ GoDaddy DNS │
│                 │     │      API         │     │             │
└─────────────────┘     └──────────────────┘     └─────────────┘
                                │
                                ▼
                        ┌──────────────┐
                        │  PostgreSQL  │
                        └──────────────┘
```
