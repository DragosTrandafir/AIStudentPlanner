from __future__ import annotations
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, CheckConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.config.database import Base
from backend.domain.enums import SubjectType, SubjectStatus


class Subject(Base):
    __tablename__ = "subjects"
    __table_args__ = (
        CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="ck_subjects_difficulty_1to5"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[SubjectType] = mapped_column(SQLEnum(SubjectType), nullable=False)
    status: Mapped[SubjectStatus] = mapped_column(SQLEnum(SubjectStatus), nullable=False, default=SubjectStatus.NOT_STARTED)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    student: Mapped["User"] = relationship(back_populates="subjects")
    ai_tasks: Mapped[List["AITask"]] = relationship(back_populates="subject", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Subject(id={self.id!r}, title={self.title!r}, name={self.name!r}, student_id={self.student_id!r})"
