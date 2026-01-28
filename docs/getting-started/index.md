# Getting Started

This guide walks you through setting up your first madewithpris.me subdomain.

## Prerequisites

- A [madewithpris.me](https://madewithpris.me) account and API key
- [Prism CLI](https://github.com/Lasse-numerous/prisme) installed (`pip install prisme`)
- A server with a public IP address (e.g., Hetzner Cloud, DigitalOcean, AWS)

## Step 1: Sign Up

1. Visit [madewithpris.me](https://madewithpris.me)
2. Create an account
3. Generate an API key from your dashboard

## Step 2: Authenticate

Store your madewithpris.me API key:

```bash
prism auth login
# Enter your API key when prompted
```

Verify your authentication:

```bash
prism auth status
```

## Step 3: Claim a Subdomain

Choose a subdomain name (3-63 characters, alphanumeric and hyphens):

```bash
prism subdomain claim myapp
```

This reserves `myapp.madewithpris.me` for your use.

## Step 4: Deploy Your App

Deploy your application to any server with a public IP. If using Prism's Hetzner integration:

```bash
prism deploy init --provider hetzner
prism deploy apply
```

Your server should listen on HTTP (port 80). Our proxy handles HTTPS termination.

## Step 5: Activate the Subdomain

Once your server is running, activate the subdomain with its IP:

```bash
# Using Prism deploy
prism subdomain activate myapp --ip $(prism deploy ip)

# Or with a known IP
prism subdomain activate myapp --ip 1.2.3.4
```

This configures our proxy to route `myapp.madewithpris.me` to your server.

## Step 6: Verify

Check that everything is working:

```bash
prism subdomain status myapp
```

Your app should now be accessible at `https://myapp.madewithpris.me`!

## How It Works

1. **Wildcard DNS**: `*.madewithpris.me` points to our proxy
2. **Your Subdomain**: When you activate, we configure routing for your subdomain
3. **HTTPS**: Our proxy terminates SSL using a wildcard certificate
4. **Your Server**: Receives HTTP traffic from our proxy

```
User → https://myapp.madewithpris.me → Our Proxy (SSL) → http://your-server:80
```

## Next Steps

- [API Reference](../api/index.md) - Learn about the REST API
- [CLI Reference](../cli/index.md) - Full command documentation
