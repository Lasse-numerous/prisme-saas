#!/bin/bash
set -e

echo "Setting up workspace: ${WORKSPACE_NAME}"

# Set up persist volume symlinks
mkdir -p /persist/venv
ln -sfn /persist/venv /workspace/.venv
mkdir -p /persist/node_modules
ln -sfn /persist/node_modules /workspace/packages/frontend/node_modules

# Backend setup
if [ -f "pyproject.toml" ]; then
    echo "Installing Python dependencies..."
    uv sync
fi

# Frontend setup
if [ -f "packages/frontend/package.json" ]; then
    echo "Installing Node dependencies..."
    cd packages/frontend && pnpm install
    cd /workspace
fi

# Prism generate (if spec exists)
if [ -f "specs/models.py" ]; then
    echo "Running prism generate..."
    uv run prism generate --no-devcontainer || true
fi

echo ""
echo "Workspace ready!"
echo "  URL: http://${WORKSPACE_NAME}.localhost"
echo ""
