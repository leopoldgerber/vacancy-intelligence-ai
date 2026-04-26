from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ValidationRun(Base):
    """Store validation run metadata.
    Args:
        """
    __tablename__ = 'validation_runs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    validation_name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    is_valid: Mapped[bool] = mapped_column(Boolean, nullable=False)
    error_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0)
    warning_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0)
    row_count: Mapped[int] = mapped_column(Integer, nullable=False)
    column_count: Mapped[int] = mapped_column(Integer, nullable=False)
    report_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    validation_issue = relationship(
        'ValidationIssue',
        back_populates='validation_run',
        uselist=False,
        cascade='all, delete-orphan',
    )
