#!/usr/bin/env bash
# Ensure the devcontainer is up and dev servers are running.
# Used by Playwright (webServer.command) and can be run manually.
set -euo pipefail

WORKSPACE_NAME="prisme-saas-main"
BASE_URL="http://${WORKSPACE_NAME}.localhost"

# 1. Check if dev servers are already responding
if curl -sf -o /dev/null "${BASE_URL}" 2>/dev/null; then
  echo "✓ Dev servers already running at ${BASE_URL}"
  exit 0
fi

# 2. Ensure devcontainer is up
echo "Starting devcontainer..."
uv run prism devcontainer up

# 3. Start dev servers in the background inside the container
echo "Starting dev servers..."
uv run prism devcontainer exec 'nohup bash -c "uv run prism dev > /tmp/prism-dev.log 2>&1 &"'

# 4. Wait for frontend to be ready
echo "Waiting for frontend at ${BASE_URL}..."
timeout=120
elapsed=0
while ! curl -sf -o /dev/null "${BASE_URL}" 2>/dev/null; do
  if [ "$elapsed" -ge "$timeout" ]; then
    echo "✗ Timed out waiting for ${BASE_URL}"
    exit 1
  fi
  sleep 2
  elapsed=$((elapsed + 2))
done

echo "✓ Dev servers ready at ${BASE_URL}"
