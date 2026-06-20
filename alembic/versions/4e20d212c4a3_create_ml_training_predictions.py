"""create ml training predictions

Revision ID: 4e20d212c4a3
Revises: 235473e50bcd
Create Date: 2026-06-19 23:30:55.438495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e20d212c4a3'
down_revision: Union[str, Sequence[str], None] = '235473e50bcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'ml_training_predictions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('ml_training_run_id', sa.Integer(), nullable=False),
        sa.Column('source_row_index', sa.Integer(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=True),
        sa.Column('vacancy_id', sa.Integer(), nullable=True),
        sa.Column('date_day', sa.Date(), nullable=True),
        sa.Column('split_name', sa.String(length=32), nullable=False),
        sa.Column('target_name', sa.String(length=128), nullable=False),
        sa.Column('actual_value', sa.Float(), nullable=False),
        sa.Column('predicted_value', sa.Float(), nullable=False),
        sa.Column('prediction_error', sa.Float(), nullable=False),
        sa.Column('absolute_error', sa.Float(), nullable=False),
        sa.Column('squared_error', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=False), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id']),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id']),
        sa.ForeignKeyConstraint(
            ['ml_training_run_id'],
            ['ml_training_runs.id'],
        ),
        sa.ForeignKeyConstraint(
            ['vacancy_id'],
            ['vacancies.vacancy_id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        'ix_ml_training_predictions_ml_training_run_id',
        'ml_training_predictions',
        ['ml_training_run_id'],
    )
    op.create_index(
        'ix_ml_training_predictions_vacancy_id',
        'ml_training_predictions',
        ['vacancy_id'],
    )
    op.create_index(
        'ix_ml_training_predictions_client_id',
        'ml_training_predictions',
        ['client_id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        'ix_ml_training_predictions_client_id',
        table_name='ml_training_predictions',
    )
    op.drop_index(
        'ix_ml_training_predictions_vacancy_id',
        table_name='ml_training_predictions',
    )
    op.drop_index(
        'ix_ml_training_predictions_ml_training_run_id',
        table_name='ml_training_predictions',
    )
    op.drop_table('ml_training_predictions')
