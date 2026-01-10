from __future__ import annotations
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.domain.subject import Subject
from .base import BaseRepository


class SubjectRepository(BaseRepository[Subject]):
    def __init__(self, session: Session):
        super().__init__(Subject, session)

    def list_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Subject]:
        stmt = (
            select(Subject)
            .where(Subject.student_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def get_by_title_for_user(self, user_id: int, title: str) -> Optional[Subject]:
        stmt = select(Subject).where(Subject.student_id == user_id, Subject.title == title)
        return self.session.scalars(stmt).first()

    def get_by_name_for_user(self, user_id: int, name: str) -> Optional[Subject]:
        """Get a subject by name (case-insensitive) for a specific user."""
        stmt = select(Subject).where(
            Subject.student_id == user_id,
            Subject.name.ilike(name)
        )
        return self.session.scalars(stmt).first()

