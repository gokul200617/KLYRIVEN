"""Initial schema — enquiries and projects tables.

Revision ID: 0001
Revises:
Create Date: 2025-10-01 00:00:00.000000

"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── enquiries ─────────────────────────────────────────────────────────────
    op.create_table(
        "enquiries",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("company", sa.String(200), nullable=True),
        sa.Column("service_interest", sa.String(100), nullable=False),
        sa.Column("estimated_budget", sa.String(50), nullable=True),
        sa.Column("timeline", sa.String(50), nullable=True),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("consent_given", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("status", sa.String(50), nullable=False, server_default="new"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Indexes on enquiries
    op.create_index("ix_enquiries_id", "enquiries", ["id"])
    op.create_index("ix_enquiries_email", "enquiries", ["email"])
    op.create_index("ix_enquiries_created_at", "enquiries", ["created_at"])

    # ── projects ──────────────────────────────────────────────────────────────
    op.create_table(
        "projects",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("slug", sa.String(200), nullable=False, unique=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("summary", sa.String(500), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("image_urls", postgresql.JSON, nullable=True, server_default=sa.text("'[]'::json")),
        sa.Column("published", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("display_order", sa.Integer, nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Indexes on projects
    op.create_index("ix_projects_id", "projects", ["id"])
    op.create_index("ix_projects_slug", "projects", ["slug"], unique=True)
    op.create_index("ix_projects_published", "projects", ["published"])
    op.create_index("ix_projects_display_order", "projects", ["display_order"])
    op.create_index("ix_projects_category", "projects", ["category"])


def downgrade() -> None:
    # Drop in reverse creation order (child tables first)
    op.drop_index("ix_projects_category", table_name="projects")
    op.drop_index("ix_projects_display_order", table_name="projects")
    op.drop_index("ix_projects_published", table_name="projects")
    op.drop_index("ix_projects_slug", table_name="projects")
    op.drop_index("ix_projects_id", table_name="projects")
    op.drop_table("projects")

    op.drop_index("ix_enquiries_created_at", table_name="enquiries")
    op.drop_index("ix_enquiries_email", table_name="enquiries")
    op.drop_index("ix_enquiries_id", table_name="enquiries")
    op.drop_table("enquiries")
