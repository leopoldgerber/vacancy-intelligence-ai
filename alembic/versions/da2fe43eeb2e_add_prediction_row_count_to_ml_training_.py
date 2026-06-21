"""add prediction row count to ml training runs

Revision ID: da2fe43eeb2e
Revises: 4e20d212c4a3
Create Date: 2026-06-21 14:28:47.728933

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da2fe43eeb2e'
down_revision: Union[str, Sequence[str], None] = '4e20d212c4a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'ml_training_runs',
        sa.Column(
            'prediction_row_count',
            sa.Integer(),
            server_default='0',
            nullable=False,
        ),
    )
    op.alter_column(
        'ml_training_runs',
        'prediction_row_count',
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('ml_training_runs', 'prediction_row_count')
