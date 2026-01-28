"""Authentik Flow Executor client.

Drives Authentik's Flow Executor API as a headless backend,
translating challenges into simple types for the frontend.
"""

from __future__ import annotations

import json
import logging
import secrets
from typing import Any

import httpx
import redis.asyncio as redis

from prisme_api.auth.config import authentik_settings

logger = logging.getLogger(__name__)

# Stage component → simple type mapping
STAGE_TYPE_MAP = {
    "ak-stage-identification": "identification",
    "ak-stage-password": "password",
    "ak-stage-authenticator-validate": "totp_verify",
    "ak-stage-authenticator-totp-setup": "totp_setup",
    "ak-stage-email": "email_verification",
    "ak-stage-prompt": "prompt",
    "ak-stage-autosubmit": "autosubmit",
    "ak-stage-access-denied": "access_denied",
    "xak-flow-redirect": "redirect",
}

FLOW_TOKEN_TTL = 600  # 10 minutes


class FlowExecutorError(Exception):
    """Error from the Authentik Flow Executor API."""


class FlowExecutorClient:
    """Client for driving Authentik flows headlessly.

    Stores Authentik session cookies in Redis keyed by an opaque flow_token.
    The frontend only sees the flow_token and translated challenge data.
    """

    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis = redis_client
        self.base_url = authentik_settings.authentik_base_url.rstrip("/")

    def _flow_url(self, flow_slug: str) -> str:
        return f"{self.base_url}/api/v3/flows/executor/{flow_slug}/"

    def _redis_key(self, flow_token: str) -> str:
        return f"authentik_flow:{flow_token}"

    async def _store_cookies(self, flow_token: str, cookies: dict[str, str]) -> None:
        await self.redis.setex(
            self._redis_key(flow_token),
            FLOW_TOKEN_TTL,
            json.dumps(cookies),
        )

    async def _load_cookies(self, flow_token: str) -> dict[str, str]:
        data = await self.redis.get(self._redis_key(flow_token))
        if not data:
            raise FlowExecutorError("Flow session expired or invalid")
        return json.loads(data)

    async def cleanup_flow(self, flow_token: str) -> None:
        """Delete the Redis session for a flow token."""
        await self.redis.delete(self._redis_key(flow_token))

    def _translate_challenge(self, body: dict[str, Any]) -> dict[str, Any]:
        """Translate an Authentik challenge response into a simpler format."""
        component = body.get("component", "")
        challenge_type = STAGE_TYPE_MAP.get(component, component)

        result: dict[str, Any] = {
            "type": challenge_type,
            "title": body.get("flow_info", {}).get("title"),
        }

        # For prompt stages, extract field definitions
        if challenge_type == "prompt":
            fields = []
            for f in body.get("fields", []):
                fields.append(
                    {
                        "name": f.get("field_key"),
                        "label": f.get("label"),
                        "type": f.get("type"),
                        "required": f.get("required", False),
                        "placeholder": f.get("placeholder", ""),
                    }
                )
            result["fields"] = fields

        # For identification, extract sources (social logins)
        if challenge_type == "identification":
            sources = []
            for s in body.get("sources", []):
                sources.append(
                    {
                        "name": s.get("name"),
                        "icon_url": s.get("icon_url"),
                    }
                )
            result["sources"] = sources
            result["password_fields"] = body.get("password_fields", False)

        # For TOTP setup, include the config URL (for QR code generation)
        if challenge_type == "totp_setup":
            result["totp_url"] = body.get("config_url")

        # For email verification
        if challenge_type == "email_verification":
            result["title"] = result["title"] or "Check your email"

        # For access denied
        if challenge_type == "access_denied":
            result["error"] = body.get("error_message", "Access denied")

        # Detect flow completion (redirect type with to=/api/v3/flows/... or response_errors)
        if body.get("type") == "redirect":
            result["type"] = "redirect"
            result["redirect_to"] = body.get("to", "")

        return result

    async def start_flow(self, flow_slug: str) -> tuple[str, dict[str, Any]]:
        """Start an Authentik flow and return (flow_token, challenge).

        Args:
            flow_slug: The Authentik flow slug to start.

        Returns:
            Tuple of (flow_token, translated challenge data).
        """
        flow_token = secrets.token_urlsafe(32)

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                self._flow_url(flow_slug),
                headers={"Accept": "application/json"},
                follow_redirects=True,
            )

            if resp.status_code not in (200, 302):
                logger.error("Flow start failed: %s %s", resp.status_code, resp.text)
                raise FlowExecutorError(f"Failed to start flow: HTTP {resp.status_code}")

            # Store cookies from Authentik
            cookies = dict(resp.cookies)
            await self._store_cookies(flow_token, cookies)

            body = resp.json()
            challenge = self._translate_challenge(body)

        return flow_token, challenge

    async def submit_flow(
        self,
        flow_token: str,
        flow_slug: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """Submit data to an Authentik flow stage.

        Args:
            flow_token: The opaque flow token from start_flow.
            flow_slug: The Authentik flow slug.
            data: Form data to submit to the current stage.

        Returns:
            Translated challenge or completion indicator.
        """
        cookies = await self._load_cookies(flow_token)

        async with httpx.AsyncClient(cookies=cookies) as client:
            resp = await client.post(
                self._flow_url(flow_slug),
                json=data,
                headers={"Accept": "application/json"},
                follow_redirects=True,
            )

            # Update stored cookies (Authentik may rotate them)
            new_cookies = dict(resp.cookies)
            if new_cookies:
                merged = {**cookies, **new_cookies}
                await self._store_cookies(flow_token, merged)

            if resp.status_code == 200:
                body = resp.json()

                # Check for response errors (e.g., invalid password)
                if body.get("response_errors"):
                    errors = body["response_errors"]
                    # Flatten error messages
                    messages = []
                    for field_errors in errors.values():
                        for err in field_errors:
                            msg = err.get("string", str(err)) if isinstance(err, dict) else str(err)
                            messages.append(msg)
                    return {
                        "completed": False,
                        "error": "; ".join(messages) if messages else "Validation error",
                        "challenge": self._translate_challenge(body),
                    }

                challenge = self._translate_challenge(body)

                # A redirect challenge to the application means flow is complete
                if challenge["type"] == "redirect":
                    await self.cleanup_flow(flow_token)
                    return {
                        "completed": True,
                        "challenge": None,
                        "redirect_to": challenge.get("redirect_to"),
                    }

                return {
                    "completed": False,
                    "challenge": challenge,
                }

            if resp.status_code == 302:
                # Redirect = flow complete
                await self.cleanup_flow(flow_token)
                return {
                    "completed": True,
                    "challenge": None,
                    "redirect_to": resp.headers.get("Location", ""),
                }

            logger.error("Flow submit failed: %s %s", resp.status_code, resp.text)
            raise FlowExecutorError(f"Flow submission failed: HTTP {resp.status_code}")
