#!/bin/bash
# Generate Authentik OAuth2 credentials and set them as GitHub secrets
# Run this once before first deploy to set up authentication

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed${NC}"
    exit 1
fi

# Check if logged in
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not logged in to GitHub CLI. Run 'gh auth login' first${NC}"
    exit 1
fi

# Get repository
REPO="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null)}"
if [ -z "$REPO" ]; then
    echo -e "${RED}Error: Could not determine repository. Pass it as argument: $0 owner/repo${NC}"
    exit 1
fi

echo -e "${GREEN}Generating Authentik OAuth2 credentials for ${REPO}${NC}"
echo ""

# Generate credentials
CLIENT_ID="madewithprisme-$(openssl rand -hex 8)"
CLIENT_SECRET=$(openssl rand -hex 32)

echo -e "${YELLOW}Generated credentials:${NC}"
echo "  Client ID: $CLIENT_ID"
echo "  Client Secret: ${CLIENT_SECRET:0:8}..."
echo ""

# Function to set secret for an environment
set_secrets_for_env() {
    local env=$1
    echo -e "${GREEN}Setting secrets for ${env} environment...${NC}"

    echo "$CLIENT_ID" | gh secret set AUTHENTIK_CLIENT_ID --env "$env" -R "$REPO"
    echo -e "  ${GREEN}✓${NC} AUTHENTIK_CLIENT_ID"

    echo "$CLIENT_SECRET" | gh secret set AUTHENTIK_CLIENT_SECRET --env "$env" -R "$REPO"
    echo -e "  ${GREEN}✓${NC} AUTHENTIK_CLIENT_SECRET"
}

# Ask which environments to configure
echo "Which environments do you want to configure?"
echo "  1) staging only"
echo "  2) production only"
echo "  3) both staging and production"
read -p "Choice [1-3]: " choice

case $choice in
    1)
        set_secrets_for_env "staging"
        ;;
    2)
        set_secrets_for_env "production"
        ;;
    3)
        set_secrets_for_env "staging"
        echo ""
        set_secrets_for_env "production"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Done!${NC}"
echo ""
echo "Next steps:"
echo "  1. Trigger a deploy: gh workflow run deploy.yml -R $REPO"
echo "  2. The Authentik blueprint will automatically configure the OAuth2 provider"
echo "  3. Your application will use these credentials for authentication"
