from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_feedback_rating_range"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ai_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ai_tasks.id", ondelete="SET NULL"), nullable=True)

    rating: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship(back_populates="feedbacks")
    ai_task: Mapped[Optional["AITask"]] = relationship(back_populates="feedback")

    def __repr__(self) -> str:
        return f"Feedback(id={self.id!r}, rating={self.rating!r}, user_id={self.user_id!r})"
