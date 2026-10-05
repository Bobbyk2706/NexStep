"""add email delivery fields to notification

Revision ID: d7a41e9b3c52
Revises: a92cf1bef6f6
Create Date: 2026-10-02
"""

from alembic import op
import sqlalchemy as sa


revision = "d7a41e9b3c52"
down_revision = "a92cf1bef6f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Non-destructive: four new nullable columns and one unique index.
    # Existing notification rows are untouched (all new columns NULL).
    op.add_column(
        "notification",
        sa.Column("dedupe_key", sa.String(length=200), nullable=True),
    )
    op.add_column(
        "notification",
        sa.Column("email_status", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "notification",
        sa.Column("email_sent_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "notification",
        sa.Column("email_error", sa.String(), nullable=True),
    )
    op.create_index(
        "ix_notification_dedupe_key",
        "notification",
        ["dedupe_key"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_notification_dedupe_key", table_name="notification")
    op.drop_column("notification", "email_error")
    op.drop_column("notification", "email_sent_at")
    op.drop_column("notification", "email_status")
    op.drop_column("notification", "dedupe_key")