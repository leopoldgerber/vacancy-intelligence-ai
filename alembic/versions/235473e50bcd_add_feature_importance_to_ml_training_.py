"""add feature importance to ml training runs

Revision ID: 235473e50bcd
Revises: 735617570d1e
Create Date: 2026-05-24 00:29:48.396435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '235473e50bcd'
down_revision: Union[str, Sequence[str], None] = '735617570d1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'ml_training_runs',
        sa.Column('feature_importance_json', sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('ml_training_runs', 'feature_importance_json')
