from __future__ import annotations
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.domain.feedback import Feedback
from backend.domain.plan import Plan
from .base import BaseRepository


class FeedbackRepository(BaseRepository[Feedback]):
    def __init__(self, session: Session):
        super().__init__(Feedback, session)

    def list_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Feedback]:
        stmt = select(Feedback).where(Feedback.user_id == user_id).order_by(Feedback.created_at.desc()).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def get_by_plan(self, plan_id: int) -> Optional[Feedback]:
        stmt = select(Feedback).where(Feedback.plan_id == plan_id)
        return self.session.scalar(stmt)

    def get_feedback_for_generation(self, user_id: int, generation_id: str) -> Optional[Feedback]:
        """Get the most recent feedback from any plan in a generation."""
        # Join with Plan to filter by generation_id
        stmt = select(Feedback).join(Plan).where(
            Feedback.user_id == user_id,
            Plan.generation_id == generation_id
        ).order_by(Feedback.created_at.desc()).limit(1)
        return self.session.scalar(stmt)

    def get_last_two_generation_feedbacks(self, user_id: int) -> tuple[Optional[Feedback], Optional[Feedback]]:
        """Get feedback from the last two schedules (by generation_id)."""
        # Get last 2 unique generation_ids with feedback
        stmt = select(Plan.generation_id).distinct().join(Feedback).where(
            Feedback.user_id == user_id,
            Plan.generation_id.isnot(None)
        ).order_by(Plan.generation_id.desc()).limit(2)
        gen_ids = self.session.scalars(stmt).all()
        
        current_feedback = None
        last_feedback = None
        
        if len(gen_ids) >= 1:
            current_feedback = self.get_feedback_for_generation(user_id, gen_ids[0])
        
        if len(gen_ids) >= 2:
            last_feedback = self.get_feedback_for_generation(user_id, gen_ids[1])
        
        return current_feedback, last_feedback