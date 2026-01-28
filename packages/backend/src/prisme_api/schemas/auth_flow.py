"""Auth flow schemas for the Flow Executor API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class FlowChallenge(BaseModel):
    """Translated Authentik flow challenge."""

    type: str
    title: str | None = None
    fields: list[dict[str, Any]] | None = None
    sources: list[dict[str, str]] | None = None
    password_fields: bool | None = None
    totp_url: str | None = None
    error: str | None = None


class FlowStartResponse(BaseModel):
    """Response from starting a flow."""

    flow_token: str
    challenge: FlowChallenge


class FlowSubmitRequest(BaseModel):
    """Request to submit data to a flow stage."""

    flow_token: str
    data: dict[str, Any]


class FlowStepResponse(BaseModel):
    """Response from a flow submission."""

    challenge: FlowChallenge | None = None
    completed: bool = False
    user: dict[str, Any] | None = None
    error: str | None = None
    redirect_to: str | None = None
