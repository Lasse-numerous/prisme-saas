# prism auth

Authentication commands for madewithpris.me.

## prism auth login

Authenticate with your madewithpris.me API key.

```bash
prism auth login
```

### Interactive Mode

When run without arguments, prompts for your API key:

```
Enter your madewithpris.me API key: prisme_live_sk_xxxxx
Verifying API key...
✓ Successfully authenticated!
```

### Credentials Storage

Credentials are stored at `~/.config/prism/credentials.json` with restrictive permissions (0600).

---

## prism auth logout

Remove stored credentials.

```bash
prism auth logout
```

### Output

```
✓ Logged out successfully
```

---

## prism auth status

Check current authentication status.

```bash
prism auth status
```

### Output (Authenticated)

```
✓ Authenticated with madewithpris.me
  API Key: prisme_live_sk_xxx...xxx (last 4 chars shown)
  Config: ~/.config/prism/credentials.json
```

### Output (Not Authenticated)

```
✗ Not authenticated
  Run 'prism auth login' to authenticate
```
