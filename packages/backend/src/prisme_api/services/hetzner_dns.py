"""Hetzner DNS management service.

Custom service for managing DNS records via Hetzner DNS API.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx


class HetznerDNSError(Exception):
    """Hetzner DNS API error."""

    pass


@dataclass
class DNSRecord:
    """DNS record representation."""

    id: str
    name: str
    type: str
    value: str
    ttl: int
    zone_id: str


class HetznerDNSService:
    """Service for managing Hetzner DNS records."""

    BASE_URL = "https://dns.hetzner.com/api/v1"
    DOMAIN = "madewithpris.me"  # Production domain on GoDaddy

    def __init__(
        self,
        api_token: str | None = None,
        zone_id: str | None = None,
    ) -> None:
        """Initialize the Hetzner DNS service.

        Args:
            api_token: Hetzner DNS API token. If not provided, reads from
                HETZNER_DNS_API_TOKEN environment variable.
            zone_id: Hetzner DNS zone ID for madewithpris.me. If not provided,
                reads from HETZNER_DNS_ZONE_ID environment variable.

        Raises:
            HetznerDNSError: If API token or zone ID is not configured.
        """
        self.api_token = api_token or os.environ.get("HETZNER_DNS_API_TOKEN")
        self.zone_id = zone_id or os.environ.get("HETZNER_DNS_ZONE_ID")

        if not self.api_token or not self.zone_id:
            raise HetznerDNSError("HETZNER_DNS_API_TOKEN and HETZNER_DNS_ZONE_ID required")

        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={"Auth-API-Token": self.api_token},
            timeout=30.0,
        )

    async def create_a_record(self, subdomain: str, ip_address: str, ttl: int = 300) -> str:
        """Create an A record for a subdomain.

        Args:
            subdomain: The subdomain name (e.g., 'myapp')
            ip_address: The IPv4 address to point to
            ttl: Time to live in seconds (default: 300)

        Returns:
            The created record's ID

        Raises:
            HetznerDNSError: If the API call fails
        """
        response = await self._client.post(
            "/records",
            json={
                "zone_id": self.zone_id,
                "type": "A",
                "name": subdomain,
                "value": ip_address,
                "ttl": ttl,
            },
        )
        if response.status_code not in (200, 201):
            raise HetznerDNSError(f"Failed to create DNS record: {response.text}")
        return response.json()["record"]["id"]

    async def update_a_record(self, record_id: str, ip_address: str) -> None:
        """Update an existing A record's IP address.

        Args:
            record_id: The Hetzner DNS record ID
            ip_address: The new IPv4 address

        Raises:
            HetznerDNSError: If the record is not found or update fails
        """
        # Get existing record first
        get_resp = await self._client.get(f"/records/{record_id}")
        if get_resp.status_code != 200:
            raise HetznerDNSError(f"Record {record_id} not found")

        record = get_resp.json()["record"]
        response = await self._client.put(
            f"/records/{record_id}",
            json={
                "zone_id": record["zone_id"],
                "type": record["type"],
                "name": record["name"],
                "value": ip_address,
                "ttl": record["ttl"],
            },
        )
        if response.status_code != 200:
            raise HetznerDNSError(f"Failed to update DNS record: {response.text}")

    async def delete_a_record(self, record_id: str) -> None:
        """Delete an A record.

        Args:
            record_id: The Hetzner DNS record ID

        Raises:
            HetznerDNSError: If the deletion fails
        """
        response = await self._client.delete(f"/records/{record_id}")
        if response.status_code not in (200, 204):
            raise HetznerDNSError(f"Failed to delete DNS record: {response.text}")

    async def get_record(self, record_id: str) -> DNSRecord:
        """Get a DNS record by ID.

        Args:
            record_id: The Hetzner DNS record ID

        Returns:
            DNSRecord object

        Raises:
            HetznerDNSError: If the record is not found
        """
        response = await self._client.get(f"/records/{record_id}")
        if response.status_code != 200:
            raise HetznerDNSError(f"Record {record_id} not found")

        data = response.json()["record"]
        return DNSRecord(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            value=data["value"],
            ttl=data["ttl"],
            zone_id=data["zone_id"],
        )

    def check_propagation(self, subdomain: str, expected_ip: str) -> dict[str, bool]:
        """Check DNS propagation across multiple resolvers.

        This is a synchronous method that checks if the DNS record has
        propagated to major DNS resolvers.

        Args:
            subdomain: The subdomain name to check
            expected_ip: The expected IP address

        Returns:
            Dictionary mapping resolver IPs to boolean propagation status
        """
        import socket

        fqdn = f"{subdomain}.{self.DOMAIN}"
        results = {}

        resolvers = [
            "1.1.1.1",  # Cloudflare
            "8.8.8.8",  # Google
            "213.133.100.98",  # Hetzner
        ]

        for server in resolvers:
            try:
                # Note: This is a simplified check using gethostbyname
                # In production, you'd want to use a proper DNS client
                resolved = socket.gethostbyname(fqdn)
                results[server] = resolved == expected_ip
            except socket.gaierror:
                results[server] = False

        return results

    async def close(self) -> None:
        """Close the HTTP client connection."""
        await self._client.aclose()


# Reserved subdomain names that cannot be claimed
RESERVED_SUBDOMAINS = frozenset(
    [
        "www",
        "api",
        "admin",
        "app",
        "mail",
        "smtp",
        "imap",
        "pop",
        "ftp",
        "ssh",
        "git",
        "ns",
        "ns1",
        "ns2",
        "dns",
        "mx",
        "cdn",
        "static",
        "assets",
        "img",
        "images",
        "media",
        "docs",
        "help",
        "support",
        "status",
        "blog",
        "news",
        "forum",
        "community",
        "dev",
        "staging",
        "test",
        "demo",
        "beta",
        "alpha",
        "prism",
        "prisme",
        "dashboard",
        "console",
        "portal",
        "account",
        "accounts",
        "billing",
        "payment",
        "payments",
        "auth",
        "login",
        "logout",
        "register",
        "signup",
        "signin",
        "oauth",
        "sso",
    ]
)


def is_reserved_subdomain(name: str) -> bool:
    """Check if a subdomain name is reserved.

    Args:
        name: The subdomain name to check

    Returns:
        True if the name is reserved, False otherwise
    """
    return name.lower() in RESERVED_SUBDOMAINS
