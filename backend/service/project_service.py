from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from backend.config.database import get_session
from backend.domain.project import Project
from backend.repository.project_repository import ProjectRepository
from backend.repository.user_repository import UserRepository


class ProjectService:
    def create_project(
        self,
        *,
        student_id: int,
        title: str,
        deadline: Optional[datetime] = None,
        estimated_effort: Optional[int] = None,
        difficulty: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Project:
        if not title or not title.strip():
            raise ValueError("Title is required")
        # defaults
        estimated_effort = 1 if estimated_effort is None else estimated_effort
        difficulty = 1 if difficulty is None else difficulty

        if estimated_effort < 0:
            raise ValueError("Estimated effort cannot be negative")
        if difficulty < 1:
            raise ValueError("Difficulty must be at least 1")
        if deadline is not None and deadline < datetime.utcnow():
            raise ValueError("Deadline cannot be in the past")

        with get_session() as session:
            # Ensure the user exists
            user_repo = UserRepository(session)
            if not user_repo.get(student_id):
                raise ValueError("Student (user) does not exist")

            repo = ProjectRepository(session)
            project = Project(
                student_id=student_id,
                title=title.strip(),
                deadline=deadline,
                estimated_effort=estimated_effort,
                difficulty=difficulty,
                description=description,
            )
            repo.add(project)
            return project

    def get_project(self, project_id: int) -> Optional[Project]:
        with get_session() as session:
            repo = ProjectRepository(session)
            return repo.get(project_id)

    def list_projects_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Project]:
        with get_session() as session:
            repo = ProjectRepository(session)
            return repo.list_for_user(user_id, offset=offset, limit=limit)
