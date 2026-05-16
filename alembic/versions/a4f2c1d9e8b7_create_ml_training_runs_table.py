"""create ml training runs table

Revision ID: a4f2c1d9e8b7
Revises: d7439a6e4c31
Create Date: 2026-05-11 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4f2c1d9e8b7'
down_revision: Union[str, Sequence[str], None] = 'd7439a6e4c31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'ml_training_runs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('training_run_name', sa.String(length=255), nullable=False),
        sa.Column('ml_dataset_run_id', sa.Integer(), nullable=True),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('model_type', sa.String(length=128), nullable=False),
        sa.Column('target_name', sa.String(length=128), nullable=False),
        sa.Column('status', sa.String(length=64), nullable=False),
        sa.Column('is_success', sa.Boolean(), nullable=False),
        sa.Column('train_row_count', sa.Integer(), nullable=False),
        sa.Column('test_row_count', sa.Integer(), nullable=False),
        sa.Column('metric_mae', sa.Float(), nullable=True),
        sa.Column('metric_rmse', sa.Float(), nullable=True),
        sa.Column('metric_r2', sa.Float(), nullable=True),
        sa.Column('model_path', sa.String(length=500), nullable=True),
        sa.Column('report_name', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id']),
        sa.ForeignKeyConstraint(['ml_dataset_run_id'], ['ml_dataset_runs.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('ml_training_runs')
