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

    def get_by_plan(self, plan_id: int) -> Optional[Feedback]:
        stmt = select(Feedback).where(Feedback.plan_id == plan_id)
        return self.session.scalar(stmt)