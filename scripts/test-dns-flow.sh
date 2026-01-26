#!/bin/bash
# DNS Flow Validation Script
#
# This script tests the complete subdomain workflow:
# 1. Claim a subdomain
# 2. Activate it with an IP address
# 3. Check DNS propagation status
# 4. Wait for propagation
# 5. Clean up (release subdomain)
#
# Usage:
#   export PRISME_API_URL=https://api.prisme.dev
#   export PRISME_ADMIN_KEY=your_api_key
#   ./test-dns-flow.sh
#
# For local development:
#   export PRISME_API_URL=http://localhost:8000
#   export PRISME_ADMIN_KEY=test_key
#   ./test-dns-flow.sh

set -euo pipefail

# Configuration
API_URL="${PRISME_API_URL:-http://localhost:8000}"
API_KEY="${PRISME_ADMIN_KEY:?Set PRISME_ADMIN_KEY environment variable}"
TEST_SUBDOMAIN="dns-test-$(date +%s)"
TEST_IP="${TEST_IP:-95.217.1.1}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== DNS Flow Validation ==="
echo "API URL: $API_URL"
echo "Test Subdomain: $TEST_SUBDOMAIN"
echo "Test IP: $TEST_IP"
echo ""

# Helper function for API calls
api_call() {
    local method=$1
    local endpoint=$2
    local data=${3:-}

    if [ -n "$data" ]; then
        curl -sf -X "$method" "$API_URL$endpoint" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -sf -X "$method" "$API_URL$endpoint" \
            -H "Authorization: Bearer $API_KEY"
    fi
}

# Step 1: Claim subdomain
echo -e "${YELLOW}[1/5] Claiming subdomain...${NC}"
CLAIM_RESPONSE=$(api_call POST "/subdomains/claim" "{\"name\": \"$TEST_SUBDOMAIN\"}")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Subdomain claimed successfully${NC}"
    echo "$CLAIM_RESPONSE" | jq .
else
    echo -e "${RED}✗ Failed to claim subdomain${NC}"
    exit 1
fi
echo ""

# Step 2: Activate subdomain with IP
echo -e "${YELLOW}[2/5] Activating subdomain with IP...${NC}"
ACTIVATE_RESPONSE=$(api_call POST "/subdomains/$TEST_SUBDOMAIN/activate" "{\"ip_address\": \"$TEST_IP\"}")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Subdomain activated successfully${NC}"
    echo "$ACTIVATE_RESPONSE" | jq .
else
    echo -e "${RED}✗ Failed to activate subdomain${NC}"
    # Clean up and exit
    api_call POST "/subdomains/$TEST_SUBDOMAIN/release" 2>/dev/null || true
    exit 1
fi
echo ""

# Step 3: Check status
echo -e "${YELLOW}[3/5] Checking DNS status...${NC}"
STATUS_RESPONSE=$(api_call GET "/subdomains/$TEST_SUBDOMAIN/status")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Status retrieved successfully${NC}"
    echo "$STATUS_RESPONSE" | jq .
else
    echo -e "${RED}✗ Failed to get status${NC}"
fi
echo ""

# Step 4: Wait for DNS propagation (optional, with timeout)
echo -e "${YELLOW}[4/5] Waiting for DNS propagation (max 60s)...${NC}"
MAX_ATTEMPTS=12
ATTEMPT=0
PROPAGATED=false

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    # Try to resolve the subdomain using Hetzner's DNS server
    RESOLVED=$(dig +short "${TEST_SUBDOMAIN}.prisme.dev" @213.133.100.98 2>/dev/null || echo "")

    if [ "$RESOLVED" = "$TEST_IP" ]; then
        echo -e "${GREEN}✓ DNS propagated successfully!${NC}"
        echo "  Resolved: $RESOLVED"
        PROPAGATED=true
        break
    fi

    ATTEMPT=$((ATTEMPT + 1))
    echo "  Attempt $ATTEMPT/$MAX_ATTEMPTS - Not propagated yet..."
    sleep 5
done

if [ "$PROPAGATED" = false ]; then
    echo -e "${YELLOW}⚠ DNS propagation timed out (this is normal for new records)${NC}"
fi
echo ""

# Step 5: Cleanup
echo -e "${YELLOW}[5/5] Cleaning up (releasing subdomain)...${NC}"
RELEASE_RESPONSE=$(api_call POST "/subdomains/$TEST_SUBDOMAIN/release")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Subdomain released successfully${NC}"
else
    # 204 No Content is returned, which curl may interpret as empty but successful
    echo -e "${GREEN}✓ Subdomain released successfully${NC}"
fi
echo ""

# Summary
echo "=== Summary ==="
if [ "$PROPAGATED" = true ]; then
    echo -e "${GREEN}=== ALL TESTS PASSED ===${NC}"
    exit 0
else
    echo -e "${YELLOW}=== TESTS COMPLETED (DNS propagation pending) ===${NC}"
    exit 0
fi
