from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from backend.domain.project import Project
from backend.repository.project_repository import ProjectRepository
from backend.repository.user_repository import UserRepository


class ProjectService:
    def __init__(self, project_repo: ProjectRepository, user_repo: UserRepository):
        self.project_repo = project_repo
        self.user_repo = user_repo

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

        # Ensure the user exists
        if not self.user_repo.get(student_id):
            raise ValueError("Student (user) does not exist")

        project = Project(
            student_id=student_id,
            title=title.strip(),
            deadline=deadline,
            estimated_effort=estimated_effort,
            difficulty=difficulty,
            description=description,
        )
        self.project_repo.add(project)
        return project

    def get_project(self, project_id: int) -> Optional[Project]:
        return self.project_repo.get(project_id)

    def list_projects_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Project]:
        return self.project_repo.list_for_user(user_id, offset=offset, limit=limit)

    def update_project(
        self,
        *,
        project_id: int,
        student_id: int,
        title: Optional[str] = None,
        deadline: Optional[datetime] = None,
        estimated_effort: Optional[int] = None,
        difficulty: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Optional[Project]:
        project = self.project_repo.get(project_id)
        if not project:
            return None

        # Verify ownership
        if project.student_id != student_id:
            raise ValueError("Project does not belong to this user")

        # Update fields if provided
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            project.title = title.strip()

        if deadline is not None:
            if deadline < datetime.utcnow():
                raise ValueError("Deadline cannot be in the past")
            project.deadline = deadline

        if estimated_effort is not None:
            if estimated_effort < 0:
                raise ValueError("Estimated effort cannot be negative")
            project.estimated_effort = estimated_effort

        if difficulty is not None:
            if difficulty < 1:
                raise ValueError("Difficulty must be at least 1")
            project.difficulty = difficulty

        if description is not None:
            project.description = description

        return project

    def delete_project(self, *, project_id: int, student_id: int) -> bool:
        project = self.project_repo.get(project_id)
        if not project:
            return False

        # Verify ownership
        if project.student_id != student_id:
            raise ValueError("Project does not belong to this user")

        self.project_repo.delete(project)
        return True