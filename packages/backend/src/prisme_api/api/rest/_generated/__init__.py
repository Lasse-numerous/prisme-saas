"""Generated REST API components."""

from .allowed_email_domain_routes import router as allowed_email_domain_base_router
from .api_key_routes import router as api_key_base_router
from .deps import DbSession, Pagination, PaginationParams, Sorting, SortParams, get_db
from .subdomain_routes import router as subdomain_base_router
from .user_routes import router as user_base_router

__all__ = [
    "DbSession",
    "Pagination",
    "PaginationParams",
    "SortParams",
    "Sorting",
    "allowed_email_domain_base_router",
    "api_key_base_router",
    "get_db",
    "subdomain_base_router",
    "user_base_router",
]
