"""MadeWithPris.me API - Managed subdomain service specification.

This spec defines the data models for the madewithpris.me managed subdomain service.
Models include:
- User: Account management with email verification and MFA
- APIKey: User-specific API keys for authentication
- Subdomain: Managed *.madewithpris.me subdomains
"""

from prism import (
    DatabaseConfig,
    FieldSpec,
    FieldType,
    FilterOperator,
    ModelSpec,
    RelationshipSpec,
    RESTExposure,
    StackSpec,
)
from prism.spec.auth import AuthConfig, AuthentikConfig, AuthentikMFAConfig, Role

spec = StackSpec(
    name="madewithprisme",
    title="MadeWithPris.me API",
    version="1.0.0",
    description="Managed subdomain service for madewithpris.me",
    database=DatabaseConfig(
        dialect="postgresql",
        async_driver=True,
    ),
    auth=AuthConfig(
        enabled=True,
        preset="authentik",
        authentik=AuthentikConfig(
            version="2024.2",
            subdomain="auth",  # auth.madewithpris.me
            mfa=AuthentikMFAConfig(
                enabled=True,
                methods=["totp", "email"],
            ),
            self_signup=True,
            email_verification=True,
        ),
        user_model="User",
        username_field="email",
        default_role="user",
        roles=[
            Role(name="admin", permissions=["*"], description="Full access"),
            Role(name="user", permissions=["own:*"], description="Access own resources"),
        ],
    ),
    models=[
        # User account model
        ModelSpec(
            name="User",
            table_name="users",
            description="User account for madewithpris.me",
            timestamps=True,
            soft_delete=True,
            fields=[
                FieldSpec(
                    name="email",
                    type=FieldType.STRING,
                    required=True,
                    unique=True,
                    max_length=255,
                    description="User email address",
                    indexed=True,
                    filter_operators=[FilterOperator.EQ, FilterOperator.LIKE],
                ),
                FieldSpec(
                    name="password_hash",
                    type=FieldType.STRING,
                    required=False,
                    max_length=255,
                    description="Hashed password (bcrypt)",
                    hidden=True,
                ),
                FieldSpec(
                    name="email_verified",
                    type=FieldType.BOOLEAN,
                    default=False,
                    required=True,
                    description="Whether email has been verified",
                ),
                FieldSpec(
                    name="email_verification_token",
                    type=FieldType.STRING,
                    required=False,
                    max_length=255,
                    description="Token for email verification",
                    hidden=True,
                ),
                FieldSpec(
                    name="mfa_enabled",
                    type=FieldType.BOOLEAN,
                    default=False,
                    required=True,
                    description="Whether MFA is enabled",
                ),
                FieldSpec(
                    name="mfa_secret",
                    type=FieldType.STRING,
                    required=False,
                    max_length=255,
                    description="TOTP MFA secret",
                    hidden=True,
                ),
                FieldSpec(
                    name="subdomain_limit",
                    type=FieldType.INTEGER,
                    default=5,
                    required=True,
                    description="Maximum number of subdomains allowed",
                ),
                FieldSpec(
                    name="is_admin",
                    type=FieldType.BOOLEAN,
                    default=False,
                    required=True,
                    description="Whether user has admin privileges",
                ),
                FieldSpec(
                    name="authentik_id",
                    type=FieldType.STRING,
                    required=False,
                    unique=True,
                    max_length=255,
                    description="Authentik user ID for SSO",
                    indexed=True,
                ),
                FieldSpec(
                    name="username",
                    type=FieldType.STRING,
                    required=False,
                    max_length=100,
                    description="Username (optional, email is primary)",
                ),
                FieldSpec(
                    name="roles",
                    type=FieldType.JSON,
                    required=True,
                    default=["user"],
                    description="User roles for authorization",
                ),
                FieldSpec(
                    name="is_active",
                    type=FieldType.BOOLEAN,
                    default=True,
                    required=True,
                    description="Whether user account is active",
                ),
            ],
            relationships=[
                RelationshipSpec(
                    name="api_keys",
                    type="one_to_many",
                    target_model="APIKey",
                    back_populates="user",
                ),
                RelationshipSpec(
                    name="subdomains",
                    type="one_to_many",
                    target_model="Subdomain",
                    back_populates="owner",
                ),
            ],
            rest=RESTExposure(
                enabled=True,
                tags=["users"],
            ),
        ),
        # API Key model for user authentication
        ModelSpec(
            name="APIKey",
            table_name="api_keys",
            description="API keys for user authentication",
            timestamps=True,
            soft_delete=False,
            fields=[
                FieldSpec(
                    name="user_id",
                    type=FieldType.FOREIGN_KEY,
                    required=True,
                    references="User",
                    description="The user who owns this API key",
                    indexed=True,
                ),
                FieldSpec(
                    name="key_hash",
                    type=FieldType.STRING,
                    required=True,
                    max_length=255,
                    description="Hashed API key (SHA256)",
                    indexed=True,
                    hidden=True,
                ),
                FieldSpec(
                    name="key_prefix",
                    type=FieldType.STRING,
                    required=True,
                    max_length=20,
                    description="API key prefix for identification (e.g., prisme_live_sk_xxx)",
                ),
                FieldSpec(
                    name="name",
                    type=FieldType.STRING,
                    required=True,
                    max_length=100,
                    description="Human-readable name for the API key",
                ),
                FieldSpec(
                    name="last_used_at",
                    type=FieldType.DATETIME,
                    required=False,
                    description="Last time this API key was used",
                ),
                FieldSpec(
                    name="expires_at",
                    type=FieldType.DATETIME,
                    required=False,
                    description="When this API key expires (null = never)",
                ),
                FieldSpec(
                    name="is_active",
                    type=FieldType.BOOLEAN,
                    default=True,
                    required=True,
                    description="Whether this API key is active",
                ),
            ],
            relationships=[
                RelationshipSpec(
                    name="user",
                    type="many_to_one",
                    target_model="User",
                    back_populates="api_keys",
                ),
            ],
            rest=RESTExposure(
                enabled=True,
                tags=["api-keys"],
            ),
        ),
        # Subdomain model with user ownership
        ModelSpec(
            name="Subdomain",
            table_name="subdomains",
            description="A managed madewithpris.me subdomain",
            timestamps=True,
            soft_delete=False,
            fields=[
                FieldSpec(
                    name="name",
                    type=FieldType.STRING,
                    required=True,
                    unique=True,
                    max_length=63,
                    min_length=3,
                    pattern=r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$",
                    description="Subdomain name (e.g., 'myapp')",
                    indexed=True,
                    filter_operators=[FilterOperator.EQ, FilterOperator.LIKE],
                ),
                FieldSpec(
                    name="owner_id",
                    type=FieldType.FOREIGN_KEY,
                    required=False,
                    references="User",
                    description="The user who owns this subdomain",
                    indexed=True,
                ),
                FieldSpec(
                    name="ip_address",
                    type=FieldType.STRING,
                    required=False,
                    max_length=45,
                    pattern=r"^(\d{1,3}\.){3}\d{1,3}$",
                    description="IPv4 address for the A record",
                ),
                FieldSpec(
                    name="status",
                    type=FieldType.ENUM,
                    enum_values=["reserved", "active", "suspended", "released"],
                    default="reserved",
                    required=True,
                    indexed=True,
                    description="Current status of the subdomain",
                ),
                FieldSpec(
                    name="dns_record_id",
                    type=FieldType.STRING,
                    required=False,
                    max_length=50,
                    description="Hetzner DNS record ID",
                ),
            ],
            relationships=[
                RelationshipSpec(
                    name="owner",
                    type="many_to_one",
                    target_model="User",
                    back_populates="subdomains",
                ),
            ],
            rest=RESTExposure(
                enabled=True,
                tags=["subdomains"],
            ),
        ),
    ],
)
