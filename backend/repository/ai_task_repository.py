from __future__ import annotations
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.domain.ai_task import AITask
from .base import BaseRepository


class AITaskRepository(BaseRepository[AITask]):
    def __init__(self, session: Session):
        super().__init__(AITask, session)

    def list_all(self, offset: int = 0, limit: int = 100) -> List[AITask]:
        stmt = select(AITask).offset(offset).limit(limit)
        return self.session.scalars(stmt).all()

    def list_for_subject(self, subject_id: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        stmt = select(AITask).where(AITask.subject_id == subject_id).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def list_for_project(self, project_id: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        stmt = select(AITask).where(AITask.project_id == project_id).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def list_by_status(self, status: str, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        stmt = select(AITask).where(AITask.status == status).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())
