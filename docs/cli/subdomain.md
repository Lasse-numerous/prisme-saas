# prism subdomain

Manage prisme.dev subdomains.

## prism subdomain list

List your claimed subdomains.

```bash
prism subdomain list
```

### Output

```
┌──────────┬───────────────┬──────────┬─────────────────────┐
│ Name     │ IP Address    │ Status   │ Created             │
├──────────┼───────────────┼──────────┼─────────────────────┤
│ myapp    │ 1.2.3.4       │ active   │ 2026-01-26 12:00:00 │
│ staging  │ -             │ reserved │ 2026-01-26 11:00:00 │
└──────────┴───────────────┴──────────┴─────────────────────┘
```

---

## prism subdomain claim

Claim a new subdomain.

```bash
prism subdomain claim NAME
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `NAME` | Yes | Subdomain name to claim |

### Example

```bash
prism subdomain claim myapp
```

### Output

```
✓ Subdomain 'myapp' claimed successfully!
  URL: https://myapp.prisme.dev (not yet active)

To activate, run:
  prism subdomain activate myapp --ip <your-server-ip>
```

### Validation Errors

```bash
prism subdomain claim a
# Error: Subdomain name must be at least 3 characters

prism subdomain claim api
# Error: 'api' is a reserved subdomain name

prism subdomain claim my_app
# Error: Subdomain name can only contain lowercase letters, numbers, and hyphens
```

---

## prism subdomain activate

Activate a subdomain by setting its IP address.

```bash
prism subdomain activate NAME --ip IP_ADDRESS
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `NAME` | Yes | Subdomain name |
| `--ip` | Yes | IPv4 address of your server |

### Example

```bash
prism subdomain activate myapp --ip 1.2.3.4
```

### Output

```
✓ Subdomain 'myapp' activated!
  URL: https://myapp.prisme.dev
  IP: 1.2.3.4

DNS propagation may take a few minutes.
Check status with: prism subdomain status myapp
```

---

## prism subdomain status

Check DNS propagation status.

```bash
prism subdomain status NAME
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `NAME` | Yes | Subdomain name |

### Example

```bash
prism subdomain status myapp
```

### Output (Propagated)

```
Subdomain: myapp.prisme.dev
Status: active
IP Address: 1.2.3.4

DNS Propagation:
  ✓ Google DNS (8.8.8.8)
  ✓ Cloudflare (1.1.1.1)
  ✓ Quad9 (9.9.9.9)

✓ DNS fully propagated! Your site should be accessible.
```

### Output (Propagating)

```
Subdomain: myapp.prisme.dev
Status: active
IP Address: 1.2.3.4

DNS Propagation:
  ✓ Google DNS (8.8.8.8)
  ✗ Cloudflare (1.1.1.1)
  ✓ Quad9 (9.9.9.9)

⏳ DNS is still propagating. This usually takes 1-5 minutes.
```

---

## prism subdomain release

Release a subdomain, making it available for others.

```bash
prism subdomain release NAME
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `NAME` | Yes | Subdomain name to release |

### Example

```bash
prism subdomain release myapp
```

### Output

```
⚠️  This will permanently release 'myapp.prisme.dev'
   The DNS record will be deleted and the subdomain will become available for others.

Are you sure? [y/N]: y

✓ Subdomain 'myapp' released successfully
```

### Flags

| Flag | Description |
|------|-------------|
| `--yes`, `-y` | Skip confirmation prompt |
