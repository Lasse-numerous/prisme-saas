# Getting Started

This guide walks you through setting up your first prisme.dev subdomain.

## Prerequisites

- A [prisme.dev](https://prisme.dev) account and API key
- [Prism CLI](https://github.com/Lasse-numerous/prisme) installed (`pip install prisme`)
- A Hetzner Cloud account (for server deployment)

## Step 1: Authenticate

Store your prisme.dev API key:

```bash
prism auth login
# Enter your API key when prompted
```

Verify your authentication:

```bash
prism auth status
```

## Step 2: Claim a Subdomain

Choose a subdomain name (3-63 characters, alphanumeric and hyphens):

```bash
prism subdomain claim myapp
```

This reserves `myapp.prisme.dev` for your use.

## Step 3: Deploy Your App

If you haven't already, initialize deployment infrastructure:

```bash
prism deploy init --provider hetzner
```

Deploy your application:

```bash
prism deploy apply
```

## Step 4: Activate the Subdomain

Once your server is running, activate the subdomain with its IP:

```bash
prism subdomain activate myapp --ip $(prism deploy ip)
```

## Step 5: Verify

Check DNS propagation status:

```bash
prism subdomain status myapp
```

Your app should now be accessible at `https://myapp.prisme.dev`!

## Next Steps

- [API Reference](../api/index.md) - Learn about the REST API
- [CLI Reference](../cli/index.md) - Full command documentation
