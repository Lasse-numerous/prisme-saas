# Deployment

This directory contains Infrastructure-as-Code for deploying to Hetzner Cloud.

> **Note**: `${PROJECT_NAME}` references throughout this document refer to the value set in your `.env` file (default: `prisme-saas`).

## Overview

- **Infrastructure**: Terraform for Hetzner Cloud VMs, networks, and volumes
- **Provisioning**: Cloud-init for server setup (Docker, nginx, firewall)
- **Deployment**: Docker Compose with GitHub Actions CI/CD

## Prerequisites

1. **Hetzner Cloud Account**
   - Create account at https://console.hetzner.cloud
   - Generate API token in Cloud Console → Security → API Tokens

2. **Terraform**
   - Install Terraform 1.5+ from https://terraform.io

3. **SSH Key**
   - Generate if needed: `ssh-keygen -t ed25519 -C "deploy@${PROJECT_NAME}"`

## Quick Start

### 1. Configure Environment

```bash
# Set Hetzner API token
export HCLOUD_TOKEN="your-api-token"

# Set SSH public key (or add to Hetzner Console manually)
export TF_VAR_ssh_public_key="$(cat ~/.ssh/id_ed25519.pub)"
export TF_VAR_hcloud_token="${HCLOUD_TOKEN}"
```

### 2. Initialize Terraform

```bash
cd terraform
terraform init
```

### 3. Deploy Staging

```bash
# Preview changes
terraform plan -var-file=staging.tfvars

# Apply changes
terraform apply -var-file=staging.tfvars
```

### 4. Configure Application

```bash
# Get staging server IP
STAGING_IP=$(terraform output -raw staging_server_ip)

# Copy environment template
scp ../env/.env.staging.template deploy@${STAGING_IP}:/opt/${PROJECT_NAME}/.env

# SSH to server and configure
ssh deploy@${STAGING_IP}
cd /opt/${PROJECT_NAME}
vim .env  # Configure secrets
```

### 5. Deploy Application

```bash
# Copy docker-compose.prod.yml to server (or use CI/CD)
scp ../../docker-compose.prod.yml deploy@${STAGING_IP}:/opt/${PROJECT_NAME}/

# On server: start application
ssh deploy@${STAGING_IP} "cd /opt/${PROJECT_NAME} && docker compose -f docker-compose.prod.yml up -d"
```

### 6. Setup SSL (Optional)

```bash
ssh deploy@${STAGING_IP}

# Run certbot for your domain
sudo certbot --nginx -d staging.madewithpris.me
```

## Deploy Production

```bash
# Deploy production infrastructure
terraform plan -var-file=production.tfvars
terraform apply -var-file=production.tfvars

# Get production IP (use floating IP if enabled)
PROD_IP=$(terraform output -raw production_floating_ip || terraform output -raw production_server_ip)
```

## Directory Structure

```
deploy/
├── README.md                    # This file
├── terraform/
│   ├── main.tf                  # Main infrastructure
│   ├── variables.tf             # Input variables
│   ├── outputs.tf               # Output values
│   ├── versions.tf              # Provider versions
│   ├── staging.tfvars           # Staging configuration
│   ├── production.tfvars        # Production configuration
│   ├── cloud-init/
│   │   └── user-data.yml        # Server provisioning script
│   └── modules/
│       ├── server/              # VM module
│       └── volume/              # Storage volume module
├── env/
│   ├── .env.staging.template    # Staging environment template
│   └── .env.production.template # Production environment template
└── scripts/
    ├── deploy.sh                # Deployment script
    ├── rollback.sh              # Rollback script
    └── setup-github-secrets.sh  # GitHub secrets setup script
```

## Server Specifications

| Environment | Server Type | vCPU | RAM  | Volume |
|-------------|-------------|------|------|--------|
| Staging     | cx11        | 1    | 2GB  | 10GB   |
| Production  | cx21        | 2    | 4GB  | 20GB   |

## Useful Commands

### Terraform

```bash
# View current state
terraform show

# Destroy staging (WARNING: deletes all data)
terraform destroy -var-file=staging.tfvars

# Import existing resource
terraform import hcloud_server.main SERVER_ID
```

### Server Management

```bash
# SSH to staging
$(terraform output -raw staging_ssh_command)

# View Docker logs
ssh deploy@STAGING_IP "cd /opt/${PROJECT_NAME} && docker compose logs -f"

# Restart application
ssh deploy@STAGING_IP "sudo systemctl restart ${PROJECT_NAME}"

# Database backup
ssh deploy@STAGING_IP "cd /opt/${PROJECT_NAME} && docker compose exec db pg_dump -U \${POSTGRES_USER} \${POSTGRES_DB} > backup.sql"
```

## CI/CD Integration

The `.github/workflows/deploy.yml` workflow automatically:

1. Builds Docker images on push to `main`
2. Pushes to GitHub Container Registry
3. Deploys to staging on push to `main` branch
4. Deploys to production only via manual workflow dispatch

### Setting Up GitHub Secrets

Use the setup script to configure all required secrets:

```bash
# Setup staging environment secrets
./scripts/setup-github-secrets.sh staging --ssh-key-path ~/.ssh/hetzner-management

# Setup production environment secrets
./scripts/setup-github-secrets.sh production --ssh-key-path ~/.ssh/hetzner-management
```

Then manually set the host IPs after terraform apply:
```bash
# Get server IP from terraform
cd terraform
STAGING_IP=$(terraform output -raw staging_server_ip)

# Set in GitHub
gh secret set STAGING_HOST --env staging -R Lasse-numerous/prisme-saas <<< "$STAGING_IP"
```

### Required GitHub Secrets

**Repository Secrets:**

| Secret | Description |
|--------|-------------|
| `SSH_PRIVATE_KEY` | SSH private key for deploy user |

**Environment Secrets (staging/production):**

| Secret | Description |
|--------|-------------|
| `STAGING_HOST` / `PRODUCTION_HOST` | Server IP address (optional if using terraform workflow) |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `DATABASE_URL` | Full database connection string |
| `SECRET_KEY` | Application secret key |
| `AUTHENTIK_SECRET_KEY` | Authentik encryption key |
| `AUTHENTIK_DB_PASSWORD` | Authentik PostgreSQL password |
| `AUTHENTIK_CLIENT_ID` | OAuth client ID (set after Authentik setup) |
| `AUTHENTIK_CLIENT_SECRET` | OAuth client secret (set after Authentik setup) |
| `AUTHENTIK_WEBHOOK_SECRET` | Webhook signature secret |
| `MCP_ADMIN_API_KEY` | MCP server admin API key |

## Troubleshooting

### Server not accessible

```bash
# Check firewall rules in Hetzner Console
# Verify security group allows ports 22, 80, 443
terraform output  # Check IP addresses
```

### Docker containers not starting

```bash
ssh deploy@SERVER_IP
cd /opt/${PROJECT_NAME}
docker compose -f docker-compose.prod.yml logs
docker compose -f docker-compose.prod.yml ps
```

### SSL certificate issues

```bash
# Check certificate status
sudo certbot certificates

# Renew certificates manually
sudo certbot renew --dry-run
```

## Security Notes

1. **Never commit secrets** - Use environment variables or secret management
2. **Rotate credentials** - Change passwords and API tokens regularly
3. **Enable firewall** - Only required ports are open (22, 80, 443)
4. **Use floating IP** - For production zero-downtime deployments
5. **Regular backups** - Database volumes should be backed up regularly

## Cost Estimation (Hetzner Cloud)

| Resource | Staging | Production |
|----------|---------|------------|
| Server   | ~€4/mo  | ~€8/mo     |
| Volume   | ~€1/mo  | ~€2/mo     |
| Floating IP | -    | ~€4/mo     |
| **Total** | ~€5/mo | ~€14/mo    |

*Prices are approximate and may vary. Check Hetzner pricing for current rates.*
