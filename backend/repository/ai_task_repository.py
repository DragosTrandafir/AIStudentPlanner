from __future__ import annotations
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.domain.ai_task import AITask
from .base import BaseRepository


class AITaskRepository(BaseRepository[AITask]):
    def __init__(self, session: Session):
        super().__init__(AITask, session)

    def get(self, entity_id: int):
        """Override to eagerly load subject relationship."""
        stmt = select(AITask).where(AITask.id == entity_id).options(joinedload(AITask.subject))
        return self.session.scalar(stmt)

    def list_all(self, offset: int = 0, limit: int = 100) -> List[AITask]:
        stmt = select(AITask).options(joinedload(AITask.subject)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).unique().all())

    def list_for_plan(self, plan_id: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        stmt = select(AITask).where(AITask.plan_id == plan_id).options(joinedload(AITask.subject)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).unique().all())

    def list_for_task(self, task_id: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        stmt = select(AITask).where(AITask.task_id == task_id).options(joinedload(AITask.subject)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).unique().all())
    
    def list_by_priority(self, priority: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        stmt = select(AITask).where(AITask.priority == priority).options(joinedload(AITask.subject)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).unique().all())
    
    def list_by_difficulty(self, difficulty: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        stmt = select(AITask).where(AITask.difficulty == difficulty).options(joinedload(AITask.subject)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).unique().all())