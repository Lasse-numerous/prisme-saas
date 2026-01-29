"""Cleanup: drop authentik_id, convert status to enum.

Revision ID: 20260129130000
Revises: 20260129120000
Create Date: 2026-01-29 13:00:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260129130000"
down_revision = "20260129120000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop authentik_id (removed from model)
    op.drop_index("ix_users_authentik_id", table_name="users")
    op.drop_column("users", "authentik_id")

    # Convert subdomain status from varchar to enum
    subdomain_status_enum = sa.Enum(
        "reserved",
        "active",
        "suspended",
        "released",
        name="subdomain_status_enum",
    )
    subdomain_status_enum.create(op.get_bind(), checkfirst=True)
    op.execute("ALTER TABLE subdomains ALTER COLUMN status DROP DEFAULT")
    op.execute(
        "ALTER TABLE subdomains ALTER COLUMN status TYPE subdomain_status_enum"
        " USING status::subdomain_status_enum"
    )
    op.execute("ALTER TABLE subdomains ALTER COLUMN status SET DEFAULT 'reserved'")


def downgrade() -> None:
    # Convert status back to varchar
    op.execute("ALTER TABLE subdomains ALTER COLUMN status TYPE VARCHAR(20) USING status::text")
    sa.Enum(name="subdomain_status_enum").drop(op.get_bind(), checkfirst=True)

    # Re-add authentik_id
    op.add_column(
        "users",
        sa.Column("authentik_id", sa.String(255), nullable=True),
    )
    op.create_index("ix_users_authentik_id", "users", ["authentik_id"], unique=True)
