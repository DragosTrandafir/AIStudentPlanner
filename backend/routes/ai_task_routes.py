from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.repository.ai_task_repository import AITaskRepository
from backend.repository.task_repository import TaskRepository
from backend.repository.project_repository import ProjectRepository
from backend.service.ai_task_service import AITaskService

router = APIRouter(prefix="/ai-tasks", tags=["ai-tasks"])


class AiTaskCreateRequest(BaseModel):
    title: str
    estimated_hours: int = 1
    task_id: int | None = None
    project_id: int | None = None
    notes: str | None = None
    mini_plan: Dict[str, Any] | None = None


class AiTaskUpdateRequest(BaseModel):
    title: str | None = None
    estimated_hours: int | None = None
    task_id: int | None = None
    project_id: int | None = None
    status: str | None = None
    scheduled_start: datetime | None = None
    scheduled_end: datetime | None = None
    mini_plan: Dict[str, Any] | None = None
    notes: str | None = None


class AiTaskResponse(BaseModel):
    id: int
    title: str
    estimated_hours: int
    task_id: int | None
    project_id: int | None
    status: str
    scheduled_start: datetime | None
    scheduled_end: datetime | None
    mini_plan: Dict[str, Any] | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[AiTaskResponse])
def list_ai_tasks():
    """List all AI tasks."""
    with get_session() as session:
        task_repo = TaskRepository(session)
        project_repo = ProjectRepository(session)
        ai_task_repo = AITaskRepository(session)
        service = AITaskService(ai_task_repo, task_repo, project_repo)
        return service.list_all()


@router.post("/", response_model=AiTaskResponse, status_code=status.HTTP_201_CREATED)
def add_ai_task(
    payload: AiTaskCreateRequest
):
    """Add a new AI task."""
    with get_session() as session:
        task_repo = TaskRepository(session)
        project_repo = ProjectRepository(session)
        ai_task_repo = AITaskRepository(session)
        service = AITaskService(ai_task_repo, task_repo, project_repo)
        try:
            task = service.create_task(
                title=payload.title,
                estimated_hours=payload.estimated_hours,
                task_id=payload.task_id,
                project_id=payload.project_id,
                mini_plan=payload.mini_plan,
                notes=payload.notes,
            )
            return task
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")
        

@router.patch("/{task_id}", response_model=AiTaskResponse)
def update_ai_task(
    task_id: int,
    payload: AiTaskUpdateRequest
):
    """Update an AI task."""
    with get_session() as session:
        service = AITaskService(
            AITaskRepository(session),
            TaskRepository(session),
            ProjectRepository(session)
        )
        try:
            return service.update_task(task_id, **payload.model_dump(exclude_none=True))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))