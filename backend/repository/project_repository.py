from __future__ import annotations
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.project import Project
from .base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: Session):
        super().__init__(Project, session)

    def list_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Project]:
        stmt = (
            select(Project)
            .where(Project.student_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def get_by_title_for_user(self, user_id: int, title: str) -> Optional[Project]:
        stmt = select(Project).where(Project.student_id == user_id, Project.title == title)
        return self.session.scalars(stmt).first()
