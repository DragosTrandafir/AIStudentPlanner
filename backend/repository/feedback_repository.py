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
        stmt = select(Feedback).where(Feedback.user_id == user_id).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def list_for_task(self, ai_task_id: int, *, offset: int = 0, limit: int = 100) -> List[Feedback]:
        stmt = select(Feedback).where(Feedback.ai_task_id == ai_task_id).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())
    
    def get_latest_feedback_by_user(self, user_id: int) -> List[Feedback]:
        stmt = (
            select(Feedback)
            .where(Feedback.user_id == user_id)
            .order_by(Feedback.created_at.desc())
            .limit(2)
        )
        return list(self.session.scalars(stmt).all())
