"""REST API routers."""

from .api_key import router as api_key_router
from .router import router
from .subdomain import router as subdomain_router
from .user import router as user_router

__all__ = [
    "api_key_router",
    "router",
    "subdomain_router",
    "user_router",
]
