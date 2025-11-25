from __future__ import annotations
from typing import Optional

from sqlalchemy import String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.config.database import Base


class AITask(Base):
    __tablename__ = "ai_tasks"
    __table_args__ = (
        CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="ck_aitasks_difficulty_range"),
        CheckConstraint("priority >= 1 AND priority <= 10", name="ck_aitasks_priority_range"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    time_allotted: Mapped[str] = mapped_column(String(50), nullable=False)
    ai_task_name: Mapped[str] = mapped_column(String(255), nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)

    subject: Mapped["Subject"] = relationship(back_populates="ai_tasks")

    def __repr__(self) -> str:
        return f"AITask(id={self.id!r}, ai_task_name={self.ai_task_name!r}, difficulty={self.difficulty!r}, priority={self.priority!r})"