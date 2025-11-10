from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class AITaskStatus:
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

    ALL = {PENDING, SCHEDULED, IN_PROGRESS, DONE, CANCELLED}


# Use JSONB when on Postgres, fallback to JSON otherwise
JSONType = JSONB().with_variant(JSON(), "sqlite")


class AITask(Base):
    __tablename__ = "ai_tasks"
    __table_args__ = (
        CheckConstraint("estimated_hours >= 0", name="ck_aitasks_hours_nonneg"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    estimated_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    subject_id: Mapped[Optional[int]] = mapped_column(ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)

    status: Mapped[str] = mapped_column(String(32), nullable=False, default=AITaskStatus.PENDING)

    scheduled_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    scheduled_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    mini_plan: Mapped[Optional[dict]] = mapped_column(JSONType, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    subject: Mapped[Optional["Subject"]] = relationship(back_populates="ai_tasks")
    project: Mapped[Optional["Project"]] = relationship(back_populates="ai_tasks")
    feedback: Mapped[Optional["Feedback"]] = relationship(back_populates="ai_task", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"AITask(id={self.id!r}, title={self.title!r}, status={self.status!r})"
