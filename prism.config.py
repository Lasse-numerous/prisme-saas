"""Prism configuration for prisme-api project."""

from prism import PrismConfig

config = PrismConfig(
    spec_path="specs/models.py",
    backend_path="src/prisme_api",
    frontend_path=None,  # API-only project
    backend_port=8000,
    database_url_env="DATABASE_URL",
    enable_mcp=False,  # Not needed for this API
    enable_graphql=False,  # REST-only API
    enable_rest=True,
)
