#!/bin/bash
# Setup GitHub secrets for prisme-saas deployment
# Usage: ./setup-github-secrets.sh <environment> [--ssh-key-path <path>]
#
# This script generates secure passwords and configures GitHub secrets
# for the specified environment (staging or production).

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
REPO="Lasse-numerous/prisme-saas"
SSH_KEY_PATH="${HOME}/.ssh/hetzner-management"

# Parse arguments
ENVIRONMENT=""
while [[ $# -gt 0 ]]; do
  case $1 in
    staging|production)
      ENVIRONMENT="$1"
      shift
      ;;
    --ssh-key-path)
      SSH_KEY_PATH="$2"
      shift 2
      ;;
    --repo)
      REPO="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 <environment> [--ssh-key-path <path>] [--repo <owner/repo>]"
      echo ""
      echo "Arguments:"
      echo "  environment    Required. Either 'staging' or 'production'"
      echo "  --ssh-key-path Path to SSH private key (default: ~/.ssh/hetzner-management)"
      echo "  --repo         GitHub repository (default: Lasse-numerous/prisme-saas)"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown argument: $1${NC}"
      exit 1
      ;;
  esac
done

if [[ -z "$ENVIRONMENT" ]]; then
  echo -e "${RED}Error: Environment is required (staging or production)${NC}"
  echo "Usage: $0 <environment> [--ssh-key-path <path>]"
  exit 1
fi

echo -e "${GREEN}Setting up GitHub secrets for ${ENVIRONMENT} environment${NC}"
echo "Repository: ${REPO}"
echo ""

# Check prerequisites
if ! command -v gh &> /dev/null; then
  echo -e "${RED}Error: gh CLI is not installed${NC}"
  exit 1
fi

if ! gh auth status &> /dev/null; then
  echo -e "${RED}Error: Not authenticated with gh. Run 'gh auth login' first${NC}"
  exit 1
fi

# Check SSH key exists
if [[ ! -f "$SSH_KEY_PATH" ]]; then
  echo -e "${RED}Error: SSH private key not found at ${SSH_KEY_PATH}${NC}"
  echo "Please specify the correct path with --ssh-key-path"
  exit 1
fi

# Generate secure passwords
echo -e "${YELLOW}Generating secure passwords...${NC}"
POSTGRES_PASSWORD=$(openssl rand -hex 16)
SECRET_KEY=$(openssl rand -hex 32)
AUTHENTIK_SECRET_KEY=$(openssl rand -base64 36)
AUTHENTIK_DB_PASSWORD=$(openssl rand -hex 16)
MCP_ADMIN_API_KEY=$(openssl rand -hex 32)
AUTHENTIK_WEBHOOK_SECRET=$(openssl rand -hex 32)

# Database URL
DATABASE_URL="postgresql+asyncpg://prisme:${POSTGRES_PASSWORD}@db:5432/prisme"

# Set repository-level SSH key (shared across environments)
echo -e "${YELLOW}Setting repository-level SSH_PRIVATE_KEY...${NC}"
gh secret set SSH_PRIVATE_KEY -R "$REPO" < "$SSH_KEY_PATH"
echo -e "${GREEN}✓ SSH_PRIVATE_KEY set${NC}"

# Set environment-specific secrets
echo -e "${YELLOW}Setting ${ENVIRONMENT} environment secrets...${NC}"

gh secret set POSTGRES_PASSWORD --env "$ENVIRONMENT" -R "$REPO" <<< "$POSTGRES_PASSWORD"
echo -e "${GREEN}✓ POSTGRES_PASSWORD${NC}"

gh secret set SECRET_KEY --env "$ENVIRONMENT" -R "$REPO" <<< "$SECRET_KEY"
echo -e "${GREEN}✓ SECRET_KEY${NC}"

gh secret set DATABASE_URL --env "$ENVIRONMENT" -R "$REPO" <<< "$DATABASE_URL"
echo -e "${GREEN}✓ DATABASE_URL${NC}"

gh secret set AUTHENTIK_SECRET_KEY --env "$ENVIRONMENT" -R "$REPO" <<< "$AUTHENTIK_SECRET_KEY"
echo -e "${GREEN}✓ AUTHENTIK_SECRET_KEY${NC}"

gh secret set AUTHENTIK_DB_PASSWORD --env "$ENVIRONMENT" -R "$REPO" <<< "$AUTHENTIK_DB_PASSWORD"
echo -e "${GREEN}✓ AUTHENTIK_DB_PASSWORD${NC}"

gh secret set MCP_ADMIN_API_KEY --env "$ENVIRONMENT" -R "$REPO" <<< "$MCP_ADMIN_API_KEY"
echo -e "${GREEN}✓ MCP_ADMIN_API_KEY${NC}"

gh secret set AUTHENTIK_WEBHOOK_SECRET --env "$ENVIRONMENT" -R "$REPO" <<< "$AUTHENTIK_WEBHOOK_SECRET"
echo -e "${GREEN}✓ AUTHENTIK_WEBHOOK_SECRET${NC}"

# Set placeholder Authentik OAuth secrets (need to be updated after Authentik setup)
gh secret set AUTHENTIK_CLIENT_ID --env "$ENVIRONMENT" -R "$REPO" <<< "placeholder-update-after-authentik-setup"
echo -e "${YELLOW}✓ AUTHENTIK_CLIENT_ID (placeholder - update after Authentik setup)${NC}"

gh secret set AUTHENTIK_CLIENT_SECRET --env "$ENVIRONMENT" -R "$REPO" <<< "placeholder-update-after-authentik-setup"
echo -e "${YELLOW}✓ AUTHENTIK_CLIENT_SECRET (placeholder - update after Authentik setup)${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}GitHub secrets configured successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Secrets set for ${ENVIRONMENT}:"
gh secret list --env "$ENVIRONMENT" -R "$REPO"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Run 'terraform apply' to create/update infrastructure"
echo "2. Set STAGING_HOST or PRODUCTION_HOST secret with server IP"
echo "3. After Authentik is running, update AUTHENTIK_CLIENT_ID and AUTHENTIK_CLIENT_SECRET"
echo "4. Push to main branch to trigger deployment"
