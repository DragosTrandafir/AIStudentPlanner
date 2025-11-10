from __future__ import annotations
from datetime import date
from typing import List, Optional

from backend.domain.subject import Subject
from backend.domain.enums import SubjectType, SubjectStatus
from backend.repository.subject_repository import SubjectRepository
from backend.repository.user_repository import UserRepository


class SubjectService:
    def __init__(self, subject_repo: SubjectRepository, user_repo: UserRepository):
        self.subject_repo = subject_repo
        self.user_repo = user_repo

    def create_subject(
        self,
        *,
        student_id: int,
        title: str,
        name: str,
        type: SubjectType,
        status: Optional[SubjectStatus] = None,
        difficulty: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        description: Optional[str] = None,
    ) -> Subject:
        if not title or not title.strip():
            raise ValueError("Title is required")
        if not name or not name.strip():
            raise ValueError("Name is required")

        # defaults
        status = status or SubjectStatus.NOT_STARTED
        difficulty = 1 if difficulty is None else difficulty

        if difficulty < 1 or difficulty > 5:
            raise ValueError("Difficulty must be between 1 and 5")

        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date cannot be after end date")

        # Ensure the user exists
        if not self.user_repo.get(student_id):
            raise ValueError("Student (user) does not exist")

        subject = Subject(
            student_id=student_id,
            title=title.strip(),
            name=name.strip(),
            type=type,
            status=status,
            difficulty=difficulty,
            start_date=start_date,
            end_date=end_date,
            description=description,
        )
        self.subject_repo.add(subject)
        return subject

    def get_subject(self, subject_id: int) -> Optional[Subject]:
        return self.subject_repo.get(subject_id)

    def list_subjects_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Subject]:
        return self.subject_repo.list_for_user(user_id, offset=offset, limit=limit)

    def update_subject(
        self,
        *,
        subject_id: int,
        student_id: int,
        title: Optional[str] = None,
        name: Optional[str] = None,
        type: Optional[SubjectType] = None,
        status: Optional[SubjectStatus] = None,
        difficulty: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        description: Optional[str] = None,
    ) -> Optional[Subject]:
        subject = self.subject_repo.get(subject_id)
        if not subject:
            return None

        # Verify ownership
        if subject.student_id != student_id:
            raise ValueError("Subject does not belong to this user")

        # Update fields if provided
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            subject.title = title.strip()

        if name is not None:
            if not name.strip():
                raise ValueError("Name cannot be empty")
            subject.name = name.strip()

        if type is not None:
            subject.type = type

        if status is not None:
            subject.status = status

        if difficulty is not None:
            if difficulty < 1 or difficulty > 5:
                raise ValueError("Difficulty must be between 1 and 5")
            subject.difficulty = difficulty

        if start_date is not None:
            subject.start_date = start_date

        if end_date is not None:
            subject.end_date = end_date

        # Validate dates if both are present
        if subject.start_date and subject.end_date and subject.start_date > subject.end_date:
            raise ValueError("Start date cannot be after end date")

        if description is not None:
            subject.description = description

        return subject

    def delete_subject(self, *, subject_id: int, student_id: int) -> bool:
        subject = self.subject_repo.get(subject_id)
        if not subject:
            return False

        # Verify ownership
        if subject.student_id != student_id:
            raise ValueError("Subject does not belong to this user")

        self.subject_repo.delete(subject)
        return True
