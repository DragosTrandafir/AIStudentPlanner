from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Dict, Any

from backend.config.database import get_session
from backend.domain.ai_task import AITask, AITaskStatus
from backend.repository.ai_task_repository import AITaskRepository
from backend.repository.project_repository import ProjectRepository
from backend.repository.subject_repository import SubjectRepository


class AITaskService:
    def create_task(
        self,
        *,
        title: str,
        estimated_hours: Optional[int] = None,
        subject_id: Optional[int] = None,
        project_id: Optional[int] = None,
        status: Optional[str] = None,
        scheduled_start: Optional[datetime] = None,
        scheduled_end: Optional[datetime] = None,
        mini_plan: Optional[Dict[str, Any]] = None,
        notes: Optional[str] = None,
    ) -> AITask:
        if not title or not title.strip():
            raise ValueError("Title is required")
        estimated_hours = 1 if estimated_hours is None else estimated_hours
        if estimated_hours < 0:
            raise ValueError("Estimated hours cannot be negative")

        status_val = status or AITaskStatus.PENDING
        if status_val not in AITaskStatus.ALL:
            raise ValueError(f"Invalid status: {status_val}")

        if scheduled_start and scheduled_end and scheduled_end < scheduled_start:
            raise ValueError("scheduled_end cannot be before scheduled_start")

        with get_session() as session:
            # Validate linked entities if provided
            if subject_id is not None:
                if not SubjectRepository(session).get(subject_id):
                    raise ValueError("Linked subject does not exist")
            if project_id is not None:
                if not ProjectRepository(session).get(project_id):
                    raise ValueError("Linked project does not exist")

            repo = AITaskRepository(session)
            task = AITask(
                title=title.strip(),
                estimated_hours=estimated_hours,
                subject_id=subject_id,
                project_id=project_id,
                status=status_val,
                scheduled_start=scheduled_start,
                scheduled_end=scheduled_end,
                mini_plan=mini_plan,
                notes=notes,
            )
            repo.add(task)
            return task

    def get_task(self, task_id: int) -> Optional[AITask]:
        with get_session() as session:
            return AITaskRepository(session).get(task_id)

    def list_for_subject(self, subject_id: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        with get_session() as session:
            return AITaskRepository(session).list_for_subject(subject_id, offset=offset, limit=limit)

    def list_for_project(self, project_id: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        with get_session() as session:
            return AITaskRepository(session).list_for_project(project_id, offset=offset, limit=limit)

    def list_by_status(self, status: str, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        if status not in AITaskStatus.ALL:
            raise ValueError("Invalid status")
        with get_session() as session:
            return AITaskRepository(session).list_by_status(status, offset=offset, limit=limit)

    def update_status(self, task_id: int, status: str) -> AITask:
        if status not in AITaskStatus.ALL:
            raise ValueError("Invalid status")
        with get_session() as session:
            repo = AITaskRepository(session)
            task = repo.get(task_id)
            if not task:
                raise ValueError("Task not found")
            task.status = status
            return task

    def schedule(self, task_id: int, *, start: Optional[datetime], end: Optional[datetime]) -> AITask:
        if start and end and end < start:
            raise ValueError("End cannot be before start")
        with get_session() as session:
            repo = AITaskRepository(session)
            task = repo.get(task_id)
            if not task:
                raise ValueError("Task not found")
            task.scheduled_start = start
            task.scheduled_end = end
            return task

    def attach_mini_plan(self, task_id: int, mini_plan: Dict[str, Any]) -> AITask:
        with get_session() as session:
            repo = AITaskRepository(session)
            task = repo.get(task_id)
            if not task:
                raise ValueError("Task not found")
            task.mini_plan = mini_plan
            return task
