"""Generated service base classes."""

from .allowed_email_domain_base import AllowedEmailDomainServiceBase
from .api_key_base import APIKeyServiceBase
from .base import ServiceBase
from .subdomain_base import SubdomainServiceBase
from .user_base import UserServiceBase

__all__ = [
    "APIKeyServiceBase",
    "AllowedEmailDomainServiceBase",
    "ServiceBase",
    "SubdomainServiceBase",
    "UserServiceBase",
]
