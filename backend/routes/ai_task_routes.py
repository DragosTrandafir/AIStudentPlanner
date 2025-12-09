from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.repository.ai_task_repository import AITaskRepository
from backend.repository.subject_repository import SubjectRepository
from backend.repository.plan_repository import PlanRepository
from backend.service.ai_task_service import AITaskService

router = APIRouter(prefix="/plans/{plan_id}/ai-tasks", tags=["ai-tasks"])


class AiTaskCreateRequest(BaseModel):
    ai_task_name: str
    time_allotted: str = Field(description="Time range in format HH:MM–HH:MM")
    difficulty: int = Field(ge=1, le=5, description="Difficulty level from 1 to 5")
    priority: int = Field(ge=1, le=10, description="Priority level from 1 to 10")
    task_id: int


class AiTaskUpdateRequest(BaseModel):
    ai_task_name: str | None = None
    time_allotted: str | None = None
    difficulty: int | None = Field(default=None, ge=1, le=5)
    priority: int | None = Field(default=None, ge=1, le=10)
    plan_id: int | None = None
    task_id: int | None = None


class AiTaskResponse(BaseModel):
    id: int
    ai_task_name: str
    task_name: str  # From Subject.name
    time_allotted: str
    difficulty: int
    priority: int
    plan_id: int
    task_id: int
    
    class Config:
        from_attributes = True

    @classmethod
    def from_ai_task(cls, ai_task):
        """Custom constructor to include task_name from subject."""
        return cls(
            id=ai_task.id,
            ai_task_name=ai_task.ai_task_name,
            task_name=ai_task.subject.name,  # Get name from Subject
            time_allotted=ai_task.time_allotted,
            difficulty=ai_task.difficulty,
            priority=ai_task.priority,
            plan_id=ai_task.plan_id,
            task_id=ai_task.task_id,
        )


@router.get("/", response_model=List[AiTaskResponse])
def list_ai_tasks_for_plan(plan_id: int):
    """List all AI tasks for a specific plan."""
    with get_session() as session:
        plan_repo = PlanRepository(session)
        
        # Check if plan exists
        if not plan_repo.get(plan_id):
            raise HTTPException(status_code=404, detail="Plan not found")
        
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session),
            plan_repo
        )
        tasks = service.list_for_plan(plan_id)
        return [AiTaskResponse.from_ai_task(task) for task in tasks]


@router.post("/", response_model=AiTaskResponse, status_code=status.HTTP_201_CREATED)
def add_ai_task(plan_id: int, payload: AiTaskCreateRequest):
    """Add a new AI task to a plan."""
    with get_session() as session:
        plan_repo = PlanRepository(session)
        
        # Check if plan exists
        if not plan_repo.get(plan_id):
            raise HTTPException(status_code=404, detail="Plan not found")
        
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session),
            plan_repo
        )
        try:
            task = service.create_task(
                ai_task_name=payload.ai_task_name,
                time_allotted=payload.time_allotted,
                difficulty=payload.difficulty,
                priority=payload.priority,
                plan_id=plan_id,
                task_id=payload.task_id,
            )
            return AiTaskResponse.from_ai_task(task)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")


@router.get("/{ai_task_id}", response_model=AiTaskResponse)
def get_ai_task(plan_id: int, ai_task_id: int):
    """Get a specific AI task."""
    with get_session() as session:
        plan_repo = PlanRepository(session)
        
        # Check if plan exists
        if not plan_repo.get(plan_id):
            raise HTTPException(status_code=404, detail="Plan not found")
        
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session),
            plan_repo
        )
        task = service.get_task(ai_task_id)
        if not task:
            raise HTTPException(status_code=404, detail="AI Task not found")
        if task.plan_id != plan_id:
            raise HTTPException(status_code=403, detail="AI Task does not belong to this plan")
        return AiTaskResponse.from_ai_task(task)


@router.patch("/{ai_task_id}", response_model=AiTaskResponse)
def update_ai_task(plan_id: int, ai_task_id: int, payload: AiTaskUpdateRequest):
    """Update an AI task."""
    with get_session() as session:
        plan_repo = PlanRepository(session)
        
        # Check if plan exists
        if not plan_repo.get(plan_id):
            raise HTTPException(status_code=404, detail="Plan not found")
        
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session),
            plan_repo
        )
        
        # Check if task exists and belongs to plan
        task = service.get_task(ai_task_id)
        if not task:
            raise HTTPException(status_code=404, detail="AI Task not found")
        if task.plan_id != plan_id:
            raise HTTPException(status_code=403, detail="AI Task does not belong to this plan")
        
        try:
            task = service.update_task(
                ai_task_id=ai_task_id,
                ai_task_name=payload.ai_task_name,
                time_allotted=payload.time_allotted,
                difficulty=payload.difficulty,
                priority=payload.priority,
                plan_id=payload.plan_id,
                task_id=payload.task_id,
            )
            if not task:
                raise HTTPException(status_code=404, detail="AI Task not found")
            return AiTaskResponse.from_ai_task(task)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{ai_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ai_task(plan_id: int, ai_task_id: int):
    """Delete an AI task."""
    with get_session() as session:
        plan_repo = PlanRepository(session)
        
        # Check if plan exists
        if not plan_repo.get(plan_id):
            raise HTTPException(status_code=404, detail="Plan not found")
        
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session),
            plan_repo
        )
        task = service.get_task(ai_task_id)
        if not task:
            raise HTTPException(status_code=404, detail="AI Task not found")
        if task.plan_id != plan_id:
            raise HTTPException(status_code=403, detail="AI Task does not belong to this plan")
        
        if not service.delete_task(ai_task_id):
            raise HTTPException(status_code=404, detail="AI Task not found")