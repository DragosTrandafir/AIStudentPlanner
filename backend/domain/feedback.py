from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, DateTime, ForeignKey, Text, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.config.database import Base


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = (
        UniqueConstraint("user_id", "generation_id", name="uc_user_generation_feedback"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    generation_id: Mapped[str] = mapped_column(String(36), nullable=False)  # UUID: References schedule/generation

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship(back_populates="feedbacks")

    def __repr__(self) -> str:
        return f"Feedback(id={self.id!r}, rating={self.rating!r}, user_id={self.user_id!r}, generation_id={self.generation_id!r})"