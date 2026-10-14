"""expand eligibility rule value column

Revision ID: f4c8a92d71e3
Revises: e5b92c7d1a38
Create Date: 2026-10-05
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f4c8a92d71e3"
down_revision: Union[str, Sequence[str], None] = "e5b92c7d1a38"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "eligibilityrule",
        "value",
        existing_type=sa.String(length=100),
        type_=sa.Text(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "eligibilityrule",
        "value",
        existing_type=sa.Text(),
        type_=sa.String(length=100),
        existing_nullable=False,
    )