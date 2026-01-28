"""REST API routers."""

from .allowed_email_domain import router as allowed_email_domain_router
from .api_key import router as api_key_router
from .router import router
from .subdomain import router as subdomain_router
from .user import router as user_router

__all__ = [
    "allowed_email_domain_router",
    "api_key_router",
    "router",
    "subdomain_router",
    "user_router",
]
