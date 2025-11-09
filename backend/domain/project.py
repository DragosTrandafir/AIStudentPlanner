from __future__ import annotations
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint("estimated_effort >= 0", name="ck_projects_effort_nonneg"),
        CheckConstraint("difficulty >= 1", name="ck_projects_difficulty_min1"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    estimated_effort: Mapped[int] = mapped_column(Integer, nullable=False, default=1)  # hours
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    student: Mapped["User"] = relationship(back_populates="projects")
    ai_tasks: Mapped[List["AITask"]] = relationship(back_populates="project", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Project(id={self.id!r}, title={self.title!r}, student_id={self.student_id!r})"
