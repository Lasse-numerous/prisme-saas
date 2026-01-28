"""Authentication module.

Self-issued JWT sessions with Authentik Flow Executor backend.
"""

from prisme_api.auth.config import authentik_settings, get_authentik_settings
from prisme_api.auth.dependencies import (
    CurrentActiveUser,
    CurrentUser,
    create_session_jwt,
    decode_session_jwt,
    get_current_active_user,
    get_current_user,
    require_roles,
)
from prisme_api.auth.flow_executor import FlowExecutorClient, FlowExecutorError

__all__ = [
    "CurrentActiveUser",
    "CurrentUser",
    "FlowExecutorClient",
    "FlowExecutorError",
    "authentik_settings",
    "create_session_jwt",
    "decode_session_jwt",
    "get_authentik_settings",
    "get_current_active_user",
    "get_current_user",
    "require_roles",
]
