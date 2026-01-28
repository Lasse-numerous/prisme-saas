# Quick Start

Get your first subdomain running in 5 minutes.

## TL;DR

```bash
# Install Prism CLI
pip install prisme

# Authenticate
prism auth login

# Claim and activate
prism subdomain claim myapp
prism subdomain activate myapp --ip 1.2.3.4

# Done! Visit https://myapp.madewithpris.me
```

## Detailed Steps

### 1. Install Prism CLI

```bash
pip install prisme

# Or with uv
uv pip install prisme
```

### 2. Get an API Key

1. Visit [madewithpris.me](https://madewithpris.me)
2. Create an account or log in
3. Generate an API key from your dashboard

### 3. Authenticate

```bash
prism auth login
```

Enter your API key when prompted. It will be stored securely at `~/.config/prism/credentials.json`.

### 4. Claim a Subdomain

```bash
prism subdomain claim myapp
```

Subdomain names must be:

- 3-63 characters long
- Start and end with alphanumeric characters
- Contain only lowercase letters, numbers, and hyphens
- Not be reserved (e.g., `api`, `www`, `admin`)

### 5. Activate with Your Server IP

```bash
prism subdomain activate myapp --ip 1.2.3.4
```

This configures our proxy to route `myapp.madewithpris.me` to your server.

!!! tip "Server Requirements"
    Your server should listen on **HTTP port 80**. Our proxy handles HTTPS termination with a wildcard SSL certificate—you don't need to configure SSL on your server.

### 6. Verify

Check that routing is configured:

```bash
prism subdomain status myapp
```

Once active, visit `https://myapp.madewithpris.me`!

## Architecture Overview

```
┌─────────┐    HTTPS    ┌─────────────────┐    HTTP    ┌─────────────┐
│  Users  │ ──────────► │ MadeWithPris.me │ ─────────► │ Your Server │
│         │             │     Proxy       │            │  (port 80)  │
└─────────┘             └─────────────────┘            └─────────────┘
                         Wildcard SSL cert
                         *.madewithpris.me
```

- **Wildcard DNS**: All `*.madewithpris.me` subdomains point to our proxy
- **SSL Termination**: Our proxy handles HTTPS with a wildcard certificate
- **HTTP Forwarding**: Your server receives plain HTTP from our proxy
