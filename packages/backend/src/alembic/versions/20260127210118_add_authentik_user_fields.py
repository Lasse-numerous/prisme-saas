"""Add Authentik user fields.

Revision ID: 20260127210118
Revises:
Create Date: 2026-01-27 21:01:18

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260127210118"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add Authentik-related fields to users table."""
    # Add authentik_id column (unique identifier from Authentik)
    op.add_column(
        "users",
        sa.Column("authentik_id", sa.String(255), nullable=True),
    )
    op.create_index("ix_users_authentik_id", "users", ["authentik_id"], unique=True)

    # Add username column
    op.add_column(
        "users",
        sa.Column("username", sa.String(100), nullable=True),
    )

    # Add roles column (JSON array of role names)
    op.add_column(
        "users",
        sa.Column("roles", sa.JSON(), nullable=False, server_default='["user"]'),
    )

    # Add is_active column
    op.add_column(
        "users",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
    )


def downgrade() -> None:
    """Remove Authentik-related fields from users table."""
    op.drop_column("users", "is_active")
    op.drop_column("users", "roles")
    op.drop_column("users", "username")
    op.drop_index("ix_users_authentik_id", table_name="users")
    op.drop_column("users", "authentik_id")
