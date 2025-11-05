from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from backend.config.database import get_session
from backend.domain.subject import Subject
from backend.repository.subject_repository import SubjectRepository
from backend.repository.user_repository import UserRepository


class SubjectService:
    def create_subject(
        self,
        *,
        student_id: int,
        title: str,
        credits: Optional[int] = None,
        difficulty: Optional[int] = None,
        semester: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Subject:
        if not title or not title.strip():
            raise ValueError("Title is required")
        # defaults
        credits = 1 if credits is None else credits
        difficulty = 1 if difficulty is None else difficulty
        if credits < 0:
            raise ValueError("Credits cannot be negative")
        if difficulty < 1:
            raise ValueError("Difficulty must be at least 1")

        with get_session() as session:
            # Ensure the user exists
            user_repo = UserRepository(session)
            if not user_repo.get(student_id):
                raise ValueError("Student (user) does not exist")

            repo = SubjectRepository(session)
            subject = Subject(
                student_id=student_id,
                title=title.strip(),
                credits=credits,
                difficulty=difficulty,
                semester=semester,
                description=description,
            )
            repo.add(subject)
            return subject

    def get_subject(self, subject_id: int) -> Optional[Subject]:
        with get_session() as session:
            repo = SubjectRepository(session)
            return repo.get(subject_id)

    def list_subjects_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Subject]:
        with get_session() as session:
            repo = SubjectRepository(session)
            return repo.list_for_user(user_id, offset=offset, limit=limit)
