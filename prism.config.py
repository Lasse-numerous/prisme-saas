"""Prism configuration for prisme-api project."""

from prism import PrismConfig

config = PrismConfig(
    spec_path="specs/models.py",
    backend_path="packages/backend/src/prisme_api",
    frontend_path="packages/frontend",
    backend_port=8000,
    database_url_env="DATABASE_URL",
    enable_mcp=True,
    enable_graphql=True,
    enable_rest=True,
)
