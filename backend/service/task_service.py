from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from backend.domain.task import Task
from backend.domain.enums import TaskType, TaskStatus
from backend.repository.task_repository import TaskRepository
from backend.repository.user_repository import UserRepository


class TaskService:
    def __init__(self, task_repo: TaskRepository, user_repo: UserRepository):
        self.task_repo = task_repo
        self.user_repo = user_repo

    def create_task(
        self,
        *,
        student_id: int,
        title: str,
        name: str,
        type: TaskType,
        status: Optional[TaskStatus] = None,
        difficulty: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        description: Optional[str] = None,
    ) -> Task:
        if not title or not title.strip():
            raise ValueError("Title is required")
        if not name or not name.strip():
            raise ValueError("Name is required")

        # defaults
        status = status or TaskStatus.NOT_STARTED
        difficulty = 1 if difficulty is None else difficulty

        if difficulty < 1 or difficulty > 5:
            raise ValueError("Difficulty must be between 1 and 5")

        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date cannot be after end date")

        # Ensure the user exists
        if not self.user_repo.get(student_id):
            raise ValueError("Student (user) does not exist")

        task = Task(
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
        self.task_repo.add(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.task_repo.get(task_id)

    def list_tasks_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Task]:
        return self.task_repo.list_for_user(user_id, offset=offset, limit=limit)

    def update_task(
        self,
        *,
        task_id: int,
        student_id: int,
        title: Optional[str] = None,
        name: Optional[str] = None,
        type: Optional[TaskType] = None,
        status: Optional[TaskStatus] = None,
        difficulty: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        description: Optional[str] = None,
    ) -> Optional[Task]:
        task = self.task_repo.get(task_id)
        if not task:
            return None

        # Verify ownership
        if task.student_id != student_id:
            raise ValueError("Task does not belong to this user")

        # Update fields if provided
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            task.title = title.strip()

        if name is not None:
            if not name.strip():
                raise ValueError("Name cannot be empty")
            task.name = name.strip()

        if type is not None:
            task.type = type

        if status is not None:
            task.status = status

        if difficulty is not None:
            if difficulty < 1 or difficulty > 5:
                raise ValueError("Difficulty must be between 1 and 5")
            task.difficulty = difficulty

        if start_date is not None:
            task.start_date = start_date

        if end_date is not None:
            task.end_date = end_date

        # Validate dates if both are present
        if task.start_date and task.end_date and task.start_date > task.end_date:
            raise ValueError("Start date cannot be after end date")

        if description is not None:
            task.description = description

        return task

    def delete_task(self, *, task_id: int, student_id: int) -> bool:
        task = self.task_repo.get(task_id)
        if not task:
            return False

        # Verify ownership
        if task.student_id != student_id:
            raise ValueError("Task does not belong to this user")

        self.task_repo.delete(task)
        return True
