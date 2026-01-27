# Prism Deploy Feedback

Lessons learned from deploying prisme-saas with `prism deploy init`.

## Issues Encountered

### 1. Duplicate Terraform Provider Configuration
**Problem:** `main.tf` and `versions.tf` both had `required_providers` blocks, causing Terraform init to fail.

**Fix needed in prism:** Only define `required_providers` in `versions.tf`, not in `main.tf`.

### 2. Module Provider Sources Missing
**Problem:** Server and volume modules didn't specify provider source, defaulting to `hashicorp/hcloud` instead of `hetznercloud/hcloud`.

**Fix needed in prism:** Add `required_providers` block to each module:
```hcl
terraform {
  required_providers {
    hcloud = {
      source = "hetznercloud/hcloud"
    }
  }
}
```

### 3. Server Network Configuration Error
**Problem:** `hcloud_server_network` resource had both `network_id` and `subnet_id`, but only one is allowed.

**Fix needed in prism:** Remove `network_id` from server module, only use `subnet_id`:
```hcl
resource "hcloud_server_network" "main" {
  server_id = hcloud_server.main.id
  subnet_id = var.subnet_id
}
```

### 4. Deprecated Server Types
**Problem:** Server types `cx11`, `cx21`, etc. are deprecated. Hetzner renamed them to:
- `cpx11`, `cpx21` (AMD shared)
- `cax11`, `cax21` (ARM - cheapest)
- `cx22`, `cx32` (Intel shared)

**Fix needed in prism:** Update default server types and add validation:
```hcl
variable "staging_server_type" {
  default = "cax11"  # ARM is cheapest and widely available
}
```

### 5. SSH Key Already Exists
**Problem:** If user has an existing SSH key in Hetzner with same fingerprint but different name, Terraform fails with uniqueness error.

**Fix suggestion for prism:** Either:
- Use a data source to find existing key by fingerprint
- Add option to import existing key
- Use unique project-prefixed key names

### 6. Cloud-init Deploy User SSH Keys
**Problem:** Cloud-init had `ssh_authorized_keys: []` (empty), so deploy user couldn't SSH in.

**Fix needed in prism:** The SSH key is passed via Hetzner's `ssh_keys` parameter on the server resource, but cloud-init should copy root's authorized_keys to deploy user:
```yaml
runcmd:
  - mkdir -p /home/deploy/.ssh
  - cp /root/.ssh/authorized_keys /home/deploy/.ssh/
  - chown -R deploy:deploy /home/deploy/.ssh
  - chmod 700 /home/deploy/.ssh
  - chmod 600 /home/deploy/.ssh/authorized_keys
```

## Suggested Improvements

### 1. Add .env Support for Terraform
Create a helper script or document pattern for loading `.env` file:
```bash
# deploy/scripts/load-env.sh
#!/bin/bash
set -a
source ../../.env
export TF_VAR_hcloud_token="$HCLOUD_TOKEN"
export TF_VAR_ssh_public_key="$(cat $SSH_PUBLIC_KEY_PATH)"
set +a
```

### 2. Add Server Type Discovery
Add a prism command to list available server types:
```bash
prism deploy server-types --location nbg1
```

### 3. Separate Image Building from Deployment
Two modes:
1. **CI/CD mode** - Images built by GitHub Actions, pulled by server
2. **Local mode** - Code synced to server, images built locally (useful for staging/testing)

### 4. Add GitHub Repository Setup
If GitHub deployment is chosen:
```bash
prism deploy github-setup  # Creates repo, adds secrets, configures workflow
```

### 5. Generate ARM-compatible Dockerfiles
When ARM server type (cax*) is selected, ensure Dockerfiles use ARM-compatible base images.

## What Could Be Scripted

### 1. Full Deployment Script
```bash
#!/bin/bash
# deploy/scripts/full-deploy.sh

# Load environment
source .env
export TF_VAR_hcloud_token="$HCLOUD_TOKEN"
export TF_VAR_ssh_public_key="$(cat $SSH_PUBLIC_KEY_PATH)"

# Initialize and apply Terraform
cd deploy/terraform
terraform init
terraform apply -var-file=staging.tfvars -auto-approve

# Get server IP
SERVER_IP=$(terraform output -raw staging_server_ip)

# Wait for cloud-init
echo "Waiting for server initialization..."
sleep 60

# Setup deploy user SSH (workaround for cloud-init issue)
ssh -i $SSH_KEY_PATH root@$SERVER_IP << 'EOF'
mkdir -p /home/deploy/.ssh
cp /root/.ssh/authorized_keys /home/deploy/.ssh/
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys
EOF

# Generate and deploy .env
# ... (secret generation)

# Deploy application
# ... (docker compose up)
```

### 2. Secret Generation Script
```bash
#!/bin/bash
# deploy/scripts/generate-secrets.sh

POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d '/+=')
SECRET_KEY=$(openssl rand -hex 32)

cat << EOF
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
SECRET_KEY=$SECRET_KEY
DATABASE_URL=postgresql://app:$POSTGRES_PASSWORD@db:5432/\${PROJECT_NAME}
EOF
```

### 3. Health Check Script
```bash
#!/bin/bash
# deploy/scripts/health-check.sh

SERVER_IP=$1
MAX_RETRIES=30

for i in $(seq 1 $MAX_RETRIES); do
  if curl -sf "http://$SERVER_IP/health" > /dev/null; then
    echo "Health check passed!"
    exit 0
  fi
  echo "Waiting... ($i/$MAX_RETRIES)"
  sleep 5
done

echo "Health check failed"
exit 1
```

## Current State Summary

- **Infrastructure:** Staging server created (46.225.23.92, ARM cax11)
- **Server setup:** Docker, nginx, firewall configured via cloud-init
- **Pending:** Application deployment (need to build/push Docker images)
- **GitHub repo:** Not created yet

## Next Steps When Resuming

1. Create GitHub repository `lassethomsen/prisme-saas`
2. Push code to GitHub
3. Add GitHub secrets (STAGING_HOST, SSH_PRIVATE_KEY)
4. Push to trigger CI/CD build
5. Or: Build locally on server for quick testing
