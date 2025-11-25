from __future__ import annotations
from typing import List, Optional

from backend.domain.ai_task import AITask
from backend.repository.ai_task_repository import AITaskRepository
from backend.repository.subject_repository import SubjectRepository


class AITaskService:
    def __init__(self, ai_task_repo: AITaskRepository, subject_repo: SubjectRepository):
        self.ai_task_repo = ai_task_repo
        self.subject_repo = subject_repo

    def create_task(
        self,
        *,
        ai_task_name: str,
        time_allotted: str,
        difficulty: int,
        priority: int,
        subject_id: int,
    ) -> AITask:
        if not ai_task_name or not ai_task_name.strip():
            raise ValueError("AI task name is required")
        
        if not time_allotted or not time_allotted.strip():
            raise ValueError("Time allotted is required")
        
        if difficulty < 1 or difficulty > 5:
            raise ValueError("Difficulty must be between 1 and 5")
        
        if priority < 1 or priority > 10:
            raise ValueError("Priority must be between 1 and 10")

        # Validate subject exists
        if not self.subject_repo.get(subject_id):
            raise ValueError("Subject does not exist")

        task = AITask(
            ai_task_name=ai_task_name.strip(),
            time_allotted=time_allotted.strip(),
            difficulty=difficulty,
            priority=priority,
            subject_id=subject_id,
        )
        self.ai_task_repo.add(task)
        return task

    def get_task(self, task_id: int) -> Optional[AITask]:
        return self.ai_task_repo.get(task_id)

    def list_all(self, offset: int = 0, limit: int = 100) -> List[AITask]:
        return self.ai_task_repo.list_all(offset, limit)

    def list_for_subject(self, subject_id: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        return self.ai_task_repo.list_for_subject(subject_id, offset=offset, limit=limit)
    
    def list_by_priority(self, priority: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        if priority < 1 or priority > 10:
            raise ValueError("Priority must be between 1 and 10")
        return self.ai_task_repo.list_by_priority(priority, offset=offset, limit=limit)
    
    def list_by_difficulty(self, difficulty: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        if difficulty < 1 or difficulty > 5:
            raise ValueError("Difficulty must be between 1 and 5")
        return self.ai_task_repo.list_by_difficulty(difficulty, offset=offset, limit=limit)

    def update_task(
        self,
        *,
        task_id: int,
        ai_task_name: Optional[str] = None,
        time_allotted: Optional[str] = None,
        difficulty: Optional[int] = None,
        priority: Optional[int] = None,
        subject_id: Optional[int] = None,
    ) -> Optional[AITask]:
        task = self.ai_task_repo.get(task_id)
        if not task:
            return None

        # Update fields if provided
        if ai_task_name is not None:
            if not ai_task_name.strip():
                raise ValueError("AI task name cannot be empty")
            task.ai_task_name = ai_task_name.strip()

        if time_allotted is not None:
            if not time_allotted.strip():
                raise ValueError("Time allotted cannot be empty")
            task.time_allotted = time_allotted.strip()

        if difficulty is not None:
            if difficulty < 1 or difficulty > 5:
                raise ValueError("Difficulty must be between 1 and 5")
            task.difficulty = difficulty

        if priority is not None:
            if priority < 1 or priority > 10:
                raise ValueError("Priority must be between 1 and 10")
            task.priority = priority

        if subject_id is not None:
            if not self.subject_repo.get(subject_id):
                raise ValueError("Subject does not exist")
            task.subject_id = subject_id

        return task

    def delete_task(self, task_id: int) -> bool:
        task = self.ai_task_repo.get(task_id)
        if not task:
            return False

        self.ai_task_repo.delete(task)
        return True