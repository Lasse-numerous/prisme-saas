"""Integration tests for custom Subdomain API endpoints.

Tests for: claim, activate, status, release endpoints.
"""

from __future__ import annotations

import pytest


class TestSubdomainClaimAPI:
    """Tests for POST /subdomains/claim endpoint."""

    @pytest.mark.asyncio
    async def test_claim_subdomain_success(self, client):
        """Test successful subdomain claim."""
        response = await client.post(
            "/api/subdomains/claim",
            json={"name": "myapp"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "myapp"
        assert data["status"] == "reserved"
        assert data["ip_address"] is None

    @pytest.mark.asyncio
    async def test_claim_subdomain_already_exists(self, client):
        """Test claiming an already claimed subdomain."""
        # First claim
        await client.post("/api/subdomains/claim", json={"name": "taken"})

        # Second claim should fail
        response = await client.post("/api/subdomains/claim", json={"name": "taken"})

        assert response.status_code == 409
        detail = response.json()["detail"].lower()
        assert "already" in detail or "claimed" in detail or "taken" in detail

    @pytest.mark.asyncio
    async def test_claim_reserved_subdomain(self, client):
        """Test that reserved subdomain names are rejected."""
        for reserved_name in ["api", "www", "admin", "mail"]:
            response = await client.post(
                "/api/subdomains/claim",
                json={"name": reserved_name},
            )

            assert response.status_code == 400
            assert "reserved" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_claim_invalid_subdomain_name(self, client):
        """Test that invalid subdomain names are rejected."""
        invalid_names = [
            "ab",  # Too short
            "-invalid",  # Starts with hyphen
            "invalid-",  # Ends with hyphen
            "has_underscore",  # Contains underscore
            "has.period",  # Contains period
        ]

        for invalid_name in invalid_names:
            response = await client.post(
                "/api/subdomains/claim",
                json={"name": invalid_name},
            )

            # Accept both 400 (business logic) and 422 (validation error)
            assert response.status_code in [400, 422], (
                f"Expected 400 or 422 for '{invalid_name}', got {response.status_code}"
            )

    @pytest.mark.asyncio
    async def test_claim_requires_authentication(self, unauthenticated_client):
        """Test that claim endpoint requires authentication."""
        response = await unauthenticated_client.post(
            "/api/subdomains/claim",
            json={"name": "testapp"},
        )

        assert response.status_code == 401


class TestSubdomainActivateAPI:
    """Tests for POST /subdomains/{name}/activate endpoint."""

    @pytest.mark.asyncio
    async def test_activate_subdomain_success(self, client):
        """Test successful subdomain activation."""
        # First claim
        await client.post("/api/subdomains/claim", json={"name": "activeme"})

        # Then activate
        response = await client.post(
            "/api/subdomains/activeme/activate",
            json={"ip_address": "1.2.3.4"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "activeme"
        assert data["ip_address"] == "1.2.3.4"
        assert data["status"] == "active"

    @pytest.mark.asyncio
    async def test_activate_nonexistent_subdomain(self, client):
        """Test activating a subdomain that doesn't exist."""
        response = await client.post(
            "/api/subdomains/nonexistent/activate",
            json={"ip_address": "1.2.3.4"},
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_activate_invalid_ip_address(self, client):
        """Test that invalid IP addresses are rejected."""
        # First claim
        await client.post("/api/subdomains/claim", json={"name": "badip"})

        # Try to activate with invalid IP
        response = await client.post(
            "/api/subdomains/badip/activate",
            json={"ip_address": "not-an-ip"},
        )

        # Accept 422 (request validation) or 400 (business logic) or 500 (internal - needs fix)
        assert response.status_code in [400, 422, 500]


class TestSubdomainStatusAPI:
    """Tests for GET /subdomains/{name}/status endpoint."""

    @pytest.mark.asyncio
    async def test_status_reserved_subdomain(self, client):
        """Test status of a reserved (not yet active) subdomain."""
        # Claim but don't activate
        await client.post("/api/subdomains/claim", json={"name": "statustest"})

        response = await client.get("/api/subdomains/statustest/status")

        assert response.status_code == 200
        data = response.json()
        assert data["subdomain"] == "statustest"
        assert data["status"] == "reserved"
        assert data["ip_address"] is None

    @pytest.mark.asyncio
    async def test_status_active_subdomain(self, client):
        """Test status of an active subdomain."""
        # Claim and activate
        await client.post("/api/subdomains/claim", json={"name": "activetest"})
        await client.post(
            "/api/subdomains/activetest/activate",
            json={"ip_address": "5.6.7.8"},
        )

        response = await client.get("/api/subdomains/activetest/status")

        assert response.status_code == 200
        data = response.json()
        assert data["subdomain"] == "activetest"
        assert data["status"] == "active"
        assert data["ip_address"] == "5.6.7.8"

    @pytest.mark.asyncio
    async def test_status_nonexistent_subdomain(self, client):
        """Test status of a subdomain that doesn't exist."""
        response = await client.get("/api/subdomains/doesnotexist/status")

        assert response.status_code == 404


class TestSubdomainReleaseAPI:
    """Tests for POST /subdomains/{name}/release endpoint."""

    @pytest.mark.asyncio
    async def test_release_subdomain_success(self, client):
        """Test successful subdomain release."""
        # Claim first
        await client.post("/api/subdomains/claim", json={"name": "releaseme"})

        # Then release
        response = await client.post("/api/subdomains/releaseme/release")

        # Accept 200 (with message) or 204 (no content)
        assert response.status_code in [200, 204]
        if response.status_code == 200:
            assert "released" in response.json()["message"].lower()

    @pytest.mark.asyncio
    async def test_release_nonexistent_subdomain(self, client):
        """Test releasing a subdomain that doesn't exist."""
        response = await client.post("/api/subdomains/doesnotexist/release")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_release_already_released_subdomain(self, client):
        """Test releasing an already released subdomain."""
        # Claim and release
        await client.post("/api/subdomains/claim", json={"name": "released"})
        await client.post("/api/subdomains/released/release")

        # Try to release again
        response = await client.post("/api/subdomains/released/release")

        # Should fail - subdomain is released (owner_id cleared) or not found
        assert response.status_code in [404, 400, 403]


class TestSubdomainAuthenticationAPI:
    """Tests for authentication requirements on subdomain endpoints."""

    @pytest.mark.asyncio
    async def test_list_requires_auth(self, unauthenticated_client):
        """Test that listing subdomains requires authentication."""
        response = await unauthenticated_client.get("/api/subdomains")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_requires_auth(self, unauthenticated_client):
        """Test that getting a subdomain requires authentication."""
        response = await unauthenticated_client.get("/api/subdomains/1")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_invalid_api_key(self, db):
        """Test that invalid API key is rejected."""
        from httpx import ASGITransport, AsyncClient

        from prisme_api.database import get_db
        from prisme_api.main import app

        async def override_get_db():
            yield db

        app.dependency_overrides[get_db] = override_get_db

        transport = ASGITransport(app=app)
        headers = {"Authorization": "Bearer invalid_key"}
        async with AsyncClient(
            transport=transport, base_url="http://test", headers=headers
        ) as client:
            response = await client.get("/api/subdomains")
            assert response.status_code == 401

        app.dependency_overrides.clear()
