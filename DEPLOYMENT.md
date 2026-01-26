# Deployment Checklist

Outstanding actions to deploy prisme-saas to production.

## Prerequisites

- [ ] Hetzner Cloud account created
- [ ] Hetzner API token generated
- [ ] SSH key pair generated for deployment

## Infrastructure Setup

### 1. Configure Terraform Variables

```bash
cd deploy/terraform

# Set required environment variables
export HCLOUD_TOKEN="your-hetzner-api-token"
export TF_VAR_hcloud_token="${HCLOUD_TOKEN}"
export TF_VAR_ssh_public_key="$(cat ~/.ssh/id_ed25519.pub)"
```

### 2. Initialize and Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Deploy staging first
terraform plan -var-file=staging.tfvars
terraform apply -var-file=staging.tfvars

# Note the output IP addresses
terraform output
```

### 3. Configure Server Environment

```bash
# Get staging IP
STAGING_IP=$(terraform output -raw staging_server_ip)

# Copy environment template to server
scp ../env/.env.staging.template deploy@${STAGING_IP}:/opt/prisme-saas/.env

# SSH to server and configure secrets
ssh deploy@${STAGING_IP}
cd /opt/prisme-saas
vim .env
```

**Required .env values to configure:**
- [ ] `POSTGRES_PASSWORD` - Generate with: `openssl rand -base64 32`
- [ ] `SECRET_KEY` - Generate with: `openssl rand -hex 32`
- [ ] Update `DATABASE_URL` with the generated password

### 4. Copy Docker Compose File

```bash
scp docker-compose.prod.yml deploy@${STAGING_IP}:/opt/prisme-saas/
```

## GitHub Configuration

### 5. Add GitHub Repository Variables

Go to: Repository Settings → Secrets and variables → Actions → Variables

- [ ] `PROJECT_NAME` = `prisme-saas` (optional, has default)

### 6. Add GitHub Repository Secrets

Go to: Repository Settings → Secrets and variables → Actions → Secrets

- [ ] `STAGING_HOST` - Staging server IP address
- [ ] `PRODUCTION_HOST` - Production server IP address (after production deploy)
- [ ] `SSH_PRIVATE_KEY` - Contents of `~/.ssh/id_ed25519` (the private key)

### 7. Create GitHub Environments

Go to: Repository Settings → Environments

- [ ] Create `staging` environment
- [ ] Create `production` environment (optionally add required reviewers)

## DNS Configuration

### 8. Configure DNS Records

Point your domain to the server IPs:

- [ ] `staging.madewithpris.me` → A record → Staging server IP
- [ ] `madewithpris.me` → A record → Production server IP (or floating IP)
- [ ] `www.madewithpris.me` → CNAME → `madewithpris.me`

## SSL Setup

### 9. Setup Let's Encrypt SSL

```bash
ssh deploy@${STAGING_IP}

# Run certbot for staging
sudo certbot --nginx -d staging.madewithpris.me

# For production (after DNS is configured)
sudo certbot --nginx -d madewithpris.me -d www.madewithpris.me
```

## First Deployment

### 10. Trigger Initial Deployment

Option A: Push to trigger CI/CD
```bash
git push origin staging  # Deploys to staging
git push origin main     # Deploys to production
```

Option B: Manual deployment
```bash
ssh deploy@${STAGING_IP}
cd /opt/prisme-saas
./scripts/deploy.sh latest
```

## Production Deployment

### 11. Deploy Production Infrastructure

```bash
cd deploy/terraform

# Deploy production
terraform plan -var-file=production.tfvars
terraform apply -var-file=production.tfvars

# Get production IP
PROD_IP=$(terraform output -raw production_floating_ip)
```

### 12. Configure Production Server

Repeat steps 3-4 for production using `.env.production.template`

## Verification

- [ ] Health check passes: `curl https://staging.madewithpris.me/health`
- [ ] API responds: `curl https://staging.madewithpris.me/api/`
- [ ] Frontend loads: Open `https://staging.madewithpris.me` in browser
- [ ] GraphQL playground: `https://staging.madewithpris.me/graphql`

## Rollback (if needed)

```bash
ssh deploy@${SERVER_IP}
cd /opt/prisme-saas
./scripts/rollback.sh
```
