from __future__ import annotations
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

from sqlalchemy import Integer, Date, DateTime, ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.config.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    generation_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)  # UUID: Groups plans from same generation
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship(back_populates="plans")
    ai_tasks: Mapped[List["AITask"]] = relationship(back_populates="plan", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Plan(id={self.id!r}, user_id={self.user_id!r}, plan_date={self.plan_date!r})"