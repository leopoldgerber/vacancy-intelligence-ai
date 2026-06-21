"""add prediction diagnostics to ml training runs

Revision ID: 3869ea6d29aa
Revises: da2fe43eeb2e
Create Date: 2026-06-21 20:18:34.978905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3869ea6d29aa'
down_revision: Union[str, Sequence[str], None] = 'da2fe43eeb2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'ml_training_runs',
        sa.Column('prediction_diagnostics_json', sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('ml_training_runs', 'prediction_diagnostics_json')
