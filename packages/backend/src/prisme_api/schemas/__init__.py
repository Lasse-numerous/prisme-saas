"""Pydantic schemas for API validation."""

from .allowed_email_domain import (
    AllowedEmailDomainBase,
    AllowedEmailDomainCreate,
    AllowedEmailDomainFilter,
    AllowedEmailDomainRead,
    AllowedEmailDomainUpdate,
)
from .api_key import APIKeyBase, APIKeyCreate, APIKeyFilter, APIKeyRead, APIKeyUpdate
from .subdomain import (
    SubdomainBase,
    SubdomainCreate,
    SubdomainFilter,
    SubdomainRead,
    SubdomainUpdate,
)
from .user import UserBase, UserCreate, UserFilter, UserRead, UserUpdate

__all__ = [
    "APIKeyBase",
    "APIKeyCreate",
    "APIKeyFilter",
    "APIKeyRead",
    "APIKeyUpdate",
    "AllowedEmailDomainBase",
    "AllowedEmailDomainCreate",
    "AllowedEmailDomainFilter",
    "AllowedEmailDomainRead",
    "AllowedEmailDomainUpdate",
    "SubdomainBase",
    "SubdomainCreate",
    "SubdomainFilter",
    "SubdomainRead",
    "SubdomainUpdate",
    "UserBase",
    "UserCreate",
    "UserFilter",
    "UserRead",
    "UserUpdate",
]
