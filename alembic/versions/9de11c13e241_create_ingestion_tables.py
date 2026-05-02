"""create ingestion tables

Revision ID: 9de11c13e241
Revises: 2440a194d66a
Create Date: 2026-05-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9de11c13e241"
down_revision: Union[str, Sequence[str], None] = "2440a194d66a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "client_id",
            "name",
            name="uq_companies_client_id_name",
        ),
    )

    op.create_table(
        "vacancies",
        sa.Column("vacancy_id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("vacancy_title", sa.String(length=255), nullable=False),
        sa.Column("vacancy_description", sa.String(), nullable=False),
        sa.Column("employment_type", sa.String(length=255), nullable=True),
        sa.Column("profile", sa.String(length=255), nullable=False),
        sa.Column(
            "publication_date",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column("region", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=255), nullable=False),
        sa.Column("salary_from", sa.Integer(), nullable=True),
        sa.Column("salary_to", sa.Integer(), nullable=True),
        sa.Column("tariff", sa.String(length=255), nullable=True),
        sa.Column("work_experience", sa.String(length=255), nullable=True),
        sa.Column("work_schedule", sa.String(length=255), nullable=True),
        sa.Column("standard", sa.Integer(), nullable=False),
        sa.Column("standard_plus", sa.Integer(), nullable=False),
        sa.Column("premium", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("vacancy_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("vacancies")
    op.drop_table("companies")
