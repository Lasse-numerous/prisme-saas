"""Add subdomain port, cooldown fields and allowed_email_domains table

Revision ID: 20260128170000
Revises: 20260127210118
Create Date: 2026-01-28 17:00:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260128170000"
down_revision = "20260127210118"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to subdomains table
    op.add_column(
        "subdomains",
        sa.Column("port", sa.Integer(), nullable=False, server_default="80"),
    )
    op.add_column(
        "subdomains",
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "subdomains",
        sa.Column("cooldown_until", sa.DateTime(timezone=True), nullable=True),
    )

    # Create index on cooldown_until for efficient queries
    op.create_index(
        "ix_subdomains_cooldown_until",
        "subdomains",
        ["cooldown_until"],
        unique=False,
    )

    # Create allowed_email_domains table
    op.create_table(
        "allowed_email_domains",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("domain", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_allowed_email_domains_domain",
        "allowed_email_domains",
        ["domain"],
        unique=True,
    )


def downgrade() -> None:
    # Drop allowed_email_domains table
    op.drop_index("ix_allowed_email_domains_domain", table_name="allowed_email_domains")
    op.drop_table("allowed_email_domains")

    # Remove columns from subdomains table
    op.drop_index("ix_subdomains_cooldown_until", table_name="subdomains")
    op.drop_column("subdomains", "cooldown_until")
    op.drop_column("subdomains", "released_at")
    op.drop_column("subdomains", "port")
