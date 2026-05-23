"""add ml training metadata fields

Revision ID: 735617570d1e
Revises: a4f2c1d9e8b7
Create Date: 2026-05-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '735617570d1e'
down_revision: Union[str, Sequence[str], None] = 'a4f2c1d9e8b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'ml_training_runs',
        sa.Column('model_params_json', sa.JSON(), nullable=True),
    )
    op.add_column(
        'ml_training_runs',
        sa.Column('baseline_mae', sa.Float(), nullable=True),
    )
    op.add_column(
        'ml_training_runs',
        sa.Column('mean_target', sa.Float(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('ml_training_runs', 'mean_target')
    op.drop_column('ml_training_runs', 'baseline_mae')
    op.drop_column('ml_training_runs', 'model_params_json')
