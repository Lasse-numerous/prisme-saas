# prism subdomain

Manage madewithpris.me subdomains.

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
  URL: https://myapp.madewithpris.me (not yet active)

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

Activate a subdomain by setting its IP address. This configures our proxy to route traffic to your server.

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
  URL: https://myapp.madewithpris.me
  IP: 1.2.3.4

Your subdomain is now routing to your server.
Check status with: prism subdomain status myapp
```

---

## prism subdomain status

Check subdomain status and connectivity.

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

### Output (Active)

```
Subdomain: myapp.madewithpris.me
Status: active
IP Address: 1.2.3.4

✓ Proxy route configured
✓ Your subdomain is live at https://myapp.madewithpris.me
```

### Output (Reserved)

```
Subdomain: myapp.madewithpris.me
Status: reserved
IP Address: -

⚠️  Subdomain is reserved but not yet activated.
To activate, run: prism subdomain activate myapp --ip <your-server-ip>
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
⚠️  This will permanently release 'myapp.madewithpris.me'
   The proxy route will be removed and the subdomain will become available for others.

Are you sure? [y/N]: y

✓ Subdomain 'myapp' released successfully
```

### Flags

| Flag | Description |
|------|-------------|
| `--yes`, `-y` | Skip confirmation prompt |
