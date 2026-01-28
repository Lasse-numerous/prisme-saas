"""Traefik route manager service.

Manages dynamic Traefik route files for subdomain routing.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


class TraefikRouteError(Exception):
    """Traefik route management error."""

    pass


class TraefikRouteManager:
    """Service for managing dynamic Traefik route files.

    Generates YAML configuration files that Traefik watches
    for dynamic routing of subdomains to user servers.
    """

    DOMAIN = "madewithpris.me"

    def __init__(
        self,
        routes_dir: str | None = None,
    ) -> None:
        """Initialize the route manager.

        Args:
            routes_dir: Directory for route files. If not provided, reads from
                TRAEFIK_ROUTES_DIR environment variable.

        Raises:
            TraefikRouteError: If routes directory is not configured.
        """
        self.routes_dir = Path(
            routes_dir or os.environ.get("TRAEFIK_ROUTES_DIR", "/etc/traefik/dynamic/subdomains")
        )

        # Ensure directory exists
        if not self.routes_dir.exists():
            try:
                self.routes_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created routes directory: {self.routes_dir}")
            except OSError as e:
                raise TraefikRouteError(f"Failed to create routes directory: {e}") from e

    def _generate_route_config(
        self,
        subdomain: str,
        target_ip: str,
        port: int = 80,
    ) -> dict:
        """Generate Traefik route configuration for a subdomain.

        Args:
            subdomain: The subdomain name (e.g., 'myapp')
            target_ip: Target server IP address
            port: Target server port (default: 80)

        Returns:
            Traefik dynamic configuration dict
        """
        service_name = f"subdomain-{subdomain}"
        router_name = f"subdomain-{subdomain}"

        return {
            "http": {
                "routers": {
                    router_name: {
                        "rule": f"Host(`{subdomain}.{self.DOMAIN}`)",
                        "service": service_name,
                        "entryPoints": ["websecure"],
                        "tls": {
                            "certResolver": "letsencrypt-dns",
                        },
                        "middlewares": ["security-headers", "rate-limit"],
                    },
                },
                "services": {
                    service_name: {
                        "loadBalancer": {
                            "servers": [
                                {"url": f"http://{target_ip}:{port}"},
                            ],
                            "healthCheck": {
                                "path": "/",
                                "interval": "30s",
                                "timeout": "5s",
                            },
                        },
                    },
                },
            },
        }

    def _route_file_path(self, subdomain: str) -> Path:
        """Get the route file path for a subdomain."""
        return self.routes_dir / f"{subdomain}.yml"

    async def create_route(
        self,
        subdomain: str,
        target_ip: str,
        port: int = 80,
    ) -> None:
        """Create a route file for a subdomain.

        Args:
            subdomain: The subdomain name
            target_ip: Target server IP address
            port: Target server port

        Raises:
            TraefikRouteError: If route creation fails
        """
        route_file = self._route_file_path(subdomain)
        config = self._generate_route_config(subdomain, target_ip, port)

        try:
            with open(route_file, "w") as f:
                yaml.dump(config, f, default_flow_style=False)
            logger.info(f"Created route file for {subdomain}: {route_file}")
        except OSError as e:
            raise TraefikRouteError(f"Failed to create route file: {e}") from e

    async def update_route(
        self,
        subdomain: str,
        target_ip: str,
        port: int = 80,
    ) -> None:
        """Update an existing route file.

        This is effectively the same as create_route since we overwrite.

        Args:
            subdomain: The subdomain name
            target_ip: Target server IP address
            port: Target server port
        """
        await self.create_route(subdomain, target_ip, port)

    async def delete_route(self, subdomain: str) -> None:
        """Delete a route file for a subdomain.

        Args:
            subdomain: The subdomain name

        Raises:
            TraefikRouteError: If route deletion fails
        """
        route_file = self._route_file_path(subdomain)

        if not route_file.exists():
            logger.warning(f"Route file not found for {subdomain}: {route_file}")
            return

        try:
            route_file.unlink()
            logger.info(f"Deleted route file for {subdomain}: {route_file}")
        except OSError as e:
            raise TraefikRouteError(f"Failed to delete route file: {e}") from e

    async def route_exists(self, subdomain: str) -> bool:
        """Check if a route file exists for a subdomain.

        Args:
            subdomain: The subdomain name

        Returns:
            True if route file exists
        """
        return self._route_file_path(subdomain).exists()

    async def sync_routes(
        self,
        active_subdomains: list[dict],
    ) -> tuple[int, int]:
        """Sync all route files with the list of active subdomains.

        Creates missing routes and removes orphaned routes.

        Args:
            active_subdomains: List of dicts with 'name', 'ip_address', 'port' keys

        Returns:
            Tuple of (created_count, deleted_count)
        """
        active_names = {s["name"] for s in active_subdomains}

        # Get existing route files
        existing_files = set()
        if self.routes_dir.exists():
            existing_files = {f.stem for f in self.routes_dir.glob("*.yml")}

        created_count = 0
        deleted_count = 0

        # Create missing routes
        for subdomain_data in active_subdomains:
            name = subdomain_data["name"]
            if name not in existing_files:
                await self.create_route(
                    name,
                    subdomain_data["ip_address"],
                    subdomain_data.get("port", 80),
                )
                created_count += 1

        # Delete orphaned routes
        for name in existing_files - active_names:
            await self.delete_route(name)
            deleted_count += 1

        logger.info(f"Route sync complete: {created_count} created, {deleted_count} deleted")
        return created_count, deleted_count


def get_route_manager() -> TraefikRouteManager | None:
    """Get the route manager if configured.

    Returns None if TRAEFIK_ROUTES_DIR is not set (for development).
    """
    routes_dir = os.environ.get("TRAEFIK_ROUTES_DIR")
    if not routes_dir:
        logger.warning(
            "TRAEFIK_ROUTES_DIR not configured - route management disabled. "
            "Set TRAEFIK_ROUTES_DIR to enable Traefik route management."
        )
        return None

    try:
        return TraefikRouteManager(routes_dir)
    except TraefikRouteError as e:
        logger.error(f"Failed to initialize route manager: {e}")
        return None


__all__ = ["TraefikRouteError", "TraefikRouteManager", "get_route_manager"]
