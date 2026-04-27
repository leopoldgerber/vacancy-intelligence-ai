from datetime import datetime


from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class QualityIssue(Base):
    """Store aggregated quality issues.
    Args:
        """
    __tablename__ = 'quality_issues'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quality_run_id: Mapped[int] = mapped_column(
        ForeignKey('quality_runs.id'),
        nullable=False,
        unique=True,
    )
    missing_values_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    duplicate_row_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    empty_text_values_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    whitespace_text_values_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
    )

    quality_run = relationship(
        'QualityRun',
        back_populates='quality_issue',
    )
