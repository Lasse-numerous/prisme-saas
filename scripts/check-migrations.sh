#!/usr/bin/env bash
# Check that all SQLAlchemy model changes have corresponding alembic migrations.
# Uses a throwaway Docker postgres container — no local DB required.

set -euo pipefail

CONTAINER_NAME="prisme_migration_check_$$"
DB_PORT=54399

cleanup() {
  docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
}
trap cleanup EXIT

# Check docker is available
if ! command -v docker &>/dev/null; then
  echo "⚠ Skipping migration check: docker not available"
  exit 0
fi

# Start throwaway postgres
docker run -d --name "$CONTAINER_NAME" \
  -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=migration_check \
  -p "$DB_PORT":5432 \
  postgres:16-alpine >/dev/null 2>&1

# Wait for postgres to be ready
for i in {1..30}; do
  if docker exec "$CONTAINER_NAME" pg_isready -q 2>/dev/null; then
    break
  fi
  sleep 0.5
done

export DATABASE_URL="postgresql+asyncpg://test:test@localhost:$DB_PORT/migration_check"

cd packages/backend/src

# Apply all migrations
uv run alembic upgrade head 2>&1

# Check for model drift
if uv run alembic check 2>&1; then
  echo "✓ No unapplied model changes detected."
else
  echo ""
  echo "✗ Model changes detected without a corresponding migration!"
  echo "  Run: uv run prism db migrate -m \"description of changes\""
  echo ""
  exit 1
fi
