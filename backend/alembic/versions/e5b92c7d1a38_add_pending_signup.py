"""add pending_signup table for email verification

Revision ID: e5b92c7d1a38
Revises: d7a41e9b3c52
Create Date: 2026-10-05
"""

from alembic import op
import sqlalchemy as sa


revision = "e5b92c7d1a38"
down_revision = "d7a41e9b3c52"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Non-destructive: one brand-new table. Nothing existing is touched.
    op.create_table(
        "pending_signup",
        sa.Column("pending_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("password_hash", sa.String(length=200), nullable=False),
        sa.Column("code_hash", sa.String(length=200), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("attempts", sa.Integer(), server_default="0", nullable=False),
        sa.Column("send_count", sa.Integer(), server_default="1", nullable=False),
        sa.Column("last_sent_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("pending_id"),
    )
    op.create_index(
        "ix_pending_signup_email",
        "pending_signup",
        ["email"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_pending_signup_email", table_name="pending_signup")
    op.drop_table("pending_signup")