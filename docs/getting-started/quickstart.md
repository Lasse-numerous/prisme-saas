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

# Done! Visit https://myapp.prisme.dev
```

## Detailed Steps

### 1. Install Prism CLI

```bash
pip install prisme

# Or with uv
uv pip install prisme
```

### 2. Get an API Key

1. Visit [prisme.dev](https://prisme.dev)
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

This creates a DNS A record pointing `myapp.prisme.dev` to your server.

### 6. Configure Traefik

Your Traefik should be configured to handle Let's Encrypt certificates. The standard Prism deployment template includes this automatically.

### 7. Verify

Check propagation status:

```bash
prism subdomain status myapp
```

Once propagated, visit `https://myapp.prisme.dev`!
