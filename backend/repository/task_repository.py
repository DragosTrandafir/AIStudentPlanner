from __future__ import annotations
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.domain.task import Task
from .base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: Session):
        super().__init__(Task, session)

    def list_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Task]:
        stmt = (
            select(Task)
            .where(Task.student_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def get_by_title_for_user(self, user_id: int, title: str) -> Optional[Task]:
        stmt = select(Task).where(Task.student_id == user_id, Task.title == title)
        return self.session.scalars(stmt).first()
