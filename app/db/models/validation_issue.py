from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ValidationIssue(Base):
    """Store aggregated validation issues.
    Args:
        """
    __tablename__ = 'validation_issues'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    validation_run_id: Mapped[int] = mapped_column(
        ForeignKey('validation_runs.id'),
        nullable=False,
        unique=True,
    )
    missing_required_columns_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    empty_blocking_values_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    invalid_type_values_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    invalid_datetime_values_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    invalid_reference_values_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
    )

    validation_run = relationship(
        'ValidationRun',
        back_populates='validation_issue',
    )
