#!/bin/bash
# Bootstrap Authentik for local development
# Run this after starting the Authentik services for the first time
#
# Usage:
#   docker compose -f docker-compose.dev.yml -f docker-compose.authentik-dev.yml up -d
#   ./scripts/bootstrap-authentik-dev.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Authentik Local Development Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if docker compose is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: docker is not installed${NC}"
    exit 1
fi

# Container name
AUTHENTIK_CONTAINER="madewithprisme_authentik_server"

# Check if Authentik container is running
echo -e "${YELLOW}Checking if Authentik is running...${NC}"
if ! docker ps --format '{{.Names}}' | grep -q "^${AUTHENTIK_CONTAINER}$"; then
    echo -e "${RED}Error: Authentik container is not running.${NC}"
    echo -e "Start it with:"
    echo -e "  ${GREEN}docker compose -f docker-compose.dev.yml -f docker-compose.authentik-dev.yml up -d${NC}"
    exit 1
fi

# Wait for Authentik to be healthy
echo -e "${YELLOW}Waiting for Authentik to be healthy...${NC}"
MAX_ATTEMPTS=30
ATTEMPT=0
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    HEALTH=$(docker inspect --format='{{.State.Health.Status}}' "$AUTHENTIK_CONTAINER" 2>/dev/null || echo "unknown")
    if [ "$HEALTH" = "healthy" ]; then
        echo -e "${GREEN}Authentik is healthy!${NC}"
        break
    fi
    ATTEMPT=$((ATTEMPT + 1))
    echo -e "  Waiting... ($ATTEMPT/$MAX_ATTEMPTS) - Status: $HEALTH"
    sleep 5
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo -e "${RED}Timeout waiting for Authentik to become healthy.${NC}"
    echo -e "Check logs with: docker logs $AUTHENTIK_CONTAINER"
    exit 1
fi

# Check if this is first-time setup
INIT_FILE=".authentik_dev_initialized"
if [ -f "$INIT_FILE" ]; then
    echo -e "${YELLOW}Authentik has already been initialized.${NC}"
    echo ""
    echo -e "${GREEN}Access URLs:${NC}"
    echo -e "  App:       ${BLUE}http://madewithpris.me.localhost${NC}"
    echo -e "  Authentik: ${BLUE}http://auth.localhost:9000${NC}"
    echo ""
    echo -e "To reset and reinitialize:"
    echo -e "  1. Stop services: docker compose -f docker-compose.dev.yml -f docker-compose.authentik-dev.yml down -v"
    echo -e "  2. Remove init file: rm $INIT_FILE"
    echo -e "  3. Start services and run this script again"
    exit 0
fi

# Wait a bit more for blueprints to be applied
echo -e "${YELLOW}Waiting for blueprints to be applied...${NC}"
sleep 10

# Create recovery key for akadmin
echo -e "${YELLOW}Creating admin recovery link...${NC}"
RECOVERY_LINK=$(docker exec "$AUTHENTIK_CONTAINER" ak create_recovery_key 10 akadmin 2>/dev/null || echo "")

if [ -n "$RECOVERY_LINK" ]; then
    echo -e "${GREEN}Admin recovery link created!${NC}"
    echo ""
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}  IMPORTANT: Save this recovery link!${NC}"
    echo -e "${YELLOW}========================================${NC}"
    echo ""
    echo -e "$RECOVERY_LINK"
    echo ""
    echo -e "${YELLOW}========================================${NC}"
    echo ""

    # Save to file for reference
    echo "$RECOVERY_LINK" > .authentik_dev_recovery_link
    echo -e "${GREEN}Recovery link saved to: .authentik_dev_recovery_link${NC}"
else
    echo -e "${YELLOW}Could not create recovery link (admin may already be set up).${NC}"
fi

# Mark as initialized
touch "$INIT_FILE"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${GREEN}Access URLs:${NC}"
echo -e "  App:       ${BLUE}http://madewithpris.me.localhost${NC}"
echo -e "  Authentik: ${BLUE}http://auth.localhost:9000${NC}"
echo ""
echo -e "${GREEN}Default credentials:${NC}"
echo -e "  Username: akadmin"
echo -e "  Password: (use recovery link above to set)"
echo ""
echo -e "${GREEN}OAuth Client:${NC}"
echo -e "  Client ID:     madewithprisme-dev"
echo -e "  Client Secret: dev-secret-change-me"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo -e "  1. Open the recovery link to set admin password"
echo -e "  2. Visit http://auth.localhost:9000 to access Authentik admin"
echo -e "  3. Test login at http://madewithpris.me.localhost"
echo ""
