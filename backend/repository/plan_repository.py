from __future__ import annotations
from datetime import date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.domain.plan import Plan
from backend.domain.ai_task import AITask
from .base import BaseRepository


class PlanRepository(BaseRepository[Plan]):
    def __init__(self, session: Session):
        super().__init__(Plan, session)

    def get(self, entity_id: int):
        """Override to eagerly load ai_tasks and their subjects."""
        stmt = select(Plan).where(Plan.id == entity_id).options(
            joinedload(Plan.ai_tasks).joinedload(AITask.subject)
        )
        return self.session.scalar(stmt)

    def list_all(self, offset: int = 0, limit: int = 100) -> List[Plan]:
        stmt = select(Plan).options(
            joinedload(Plan.ai_tasks).joinedload(AITask.subject)
        ).offset(offset).limit(limit).order_by(Plan.plan_date.desc())
        return list(self.session.scalars(stmt).unique().all())

    def list_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Plan]:
        stmt = select(Plan).where(Plan.user_id == user_id).options(
            joinedload(Plan.ai_tasks).joinedload(AITask.subject)
        ).offset(offset).limit(limit).order_by(Plan.plan_date.desc())
        return list(self.session.scalars(stmt).unique().all())

    def get_by_date(self, user_id: int, plan_date: date) -> Optional[Plan]:
        stmt = select(Plan).where(Plan.user_id == user_id, Plan.plan_date == plan_date).options(
            joinedload(Plan.ai_tasks).joinedload(AITask.subject)
        )
        return self.session.scalar(stmt)