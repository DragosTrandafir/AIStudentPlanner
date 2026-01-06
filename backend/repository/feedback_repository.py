from __future__ import annotations
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.domain.feedback import Feedback
from .base import BaseRepository


class FeedbackRepository(BaseRepository[Feedback]):
    def __init__(self, session: Session):
        super().__init__(Feedback, session)

    def list_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Feedback]:
        stmt = select(Feedback).where(Feedback.user_id == user_id).order_by(Feedback.created_at.desc()).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def get_by_generation(self, user_id: int, generation_id: str) -> Optional[Feedback]:
        """Get feedback for a specific generation/schedule."""
        stmt = select(Feedback).where(
            Feedback.user_id == user_id,
            Feedback.generation_id == generation_id
        )
        return self.session.scalar(stmt)

    def get_last_two_generation_feedbacks(self, user_id: int) -> tuple[Optional[Feedback], Optional[Feedback]]:
        """Get feedback from the last two schedules (by generation_id)."""
        # Get last 2 unique generation_ids with feedback
        stmt = select(Feedback.generation_id).distinct().where(
            Feedback.user_id == user_id
        ).order_by(Feedback.generation_id.desc()).limit(2)
        gen_ids = self.session.scalars(stmt).all()
        
        current_feedback = None
        last_feedback = None
        
        if len(gen_ids) >= 1:
            current_feedback = self.get_by_generation(user_id, gen_ids[0])
        
        if len(gen_ids) >= 2:
            last_feedback = self.get_by_generation(user_id, gen_ids[1])
        
        return current_feedback, last_feedback