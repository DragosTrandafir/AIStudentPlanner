from __future__ import annotations
from typing import List, Optional

from backend.domain.ai_task import AITask
from backend.repository.ai_task_repository import AITaskRepository
from backend.repository.subject_repository import SubjectRepository
from backend.repository.plan_repository import PlanRepository


class AITaskService:
    def __init__(self, ai_task_repo: AITaskRepository, subject_repo: SubjectRepository, plan_repo: PlanRepository):
        self.ai_task_repo = ai_task_repo
        self.subject_repo = subject_repo
        self.plan_repo = plan_repo

    def create_task(
        self,
        *,
        ai_task_name: str,
        time_allotted: str,
        difficulty: int,
        priority: int,
        plan_id: int,
        task_id: int,
    ) -> AITask:
        if not ai_task_name or not ai_task_name.strip():
            raise ValueError("AI task name is required")
        
        if not time_allotted or not time_allotted.strip():
            raise ValueError("Time allotted is required")
        
        if difficulty < 1 or difficulty > 5:
            raise ValueError("Difficulty must be between 1 and 5")
        
        if priority < 1 or priority > 10:
            raise ValueError("Priority must be between 1 and 10")

        # Validate plan exists
        if not self.plan_repo.get(plan_id):
            raise ValueError("Plan does not exist")

        # Validate subject/task exists
        if not self.subject_repo.get(task_id):
            raise ValueError("Task does not exist")

        task = AITask()
        task.ai_task_name = ai_task_name.strip()
        task.time_allotted = time_allotted.strip()
        task.difficulty = difficulty
        task.priority = priority
        task.plan_id = plan_id
        task.task_id = task_id
        
        self.ai_task_repo.add(task)
        self.ai_task_repo.session.flush()
        self.ai_task_repo.session.refresh(task)
        
        return task

    def get_task(self, ai_task_id: int) -> Optional[AITask]:
        return self.ai_task_repo.get(ai_task_id)

    def list_all(self, offset: int = 0, limit: int = 100) -> List[AITask]:
        return self.ai_task_repo.list_all(offset, limit)

    def list_for_plan(self, plan_id: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        return self.ai_task_repo.list_for_plan(plan_id, offset=offset, limit=limit)

    def list_for_task(self, task_id: int, *, offset: int = 0, limit: int = 100) -> List[AITask]:
        return self.ai_task_repo.list_for_task(task_id, offset=offset, limit=limit)
    
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
        ai_task_id: int,
        ai_task_name: Optional[str] = None,
        time_allotted: Optional[str] = None,
        difficulty: Optional[int] = None,
        priority: Optional[int] = None,
        plan_id: Optional[int] = None,
        task_id: Optional[int] = None,
    ) -> Optional[AITask]:
        task = self.ai_task_repo.get(ai_task_id)
        if not task:
            return None

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

        if plan_id is not None:
            if not self.plan_repo.get(plan_id):
                raise ValueError("Plan does not exist")
            task.plan_id = plan_id

        if task_id is not None:
            if not self.subject_repo.get(task_id):
                raise ValueError("Task does not exist")
            task.task_id = task_id

        return task

    def delete_task(self, ai_task_id: int) -> bool:
        task = self.ai_task_repo.get(ai_task_id)
        if not task:
            return False

        self.ai_task_repo.delete(task)
        return True