from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.repository.ai_task_repository import AITaskRepository
from backend.repository.subject_repository import SubjectRepository
from backend.service.ai_task_service import AITaskService

router = APIRouter(prefix="/ai-tasks", tags=["ai-tasks"])


class AiTaskCreateRequest(BaseModel):
    ai_task_name: str
    time_allotted: str = Field(description="Time range in format HH:MM–HH:MM")
    difficulty: int = Field(ge=1, le=5, description="Difficulty level from 1 to 5")
    priority: int = Field(ge=1, le=10, description="Priority level from 1 to 10")
    subject_id: int


class AiTaskUpdateRequest(BaseModel):
    ai_task_name: str | None = None
    time_allotted: str | None = None
    difficulty: int | None = Field(default=None, ge=1, le=5)
    priority: int | None = Field(default=None, ge=1, le=10)
    subject_id: int | None = None


class AiTaskResponse(BaseModel):
    id: int
    ai_task_name: str
    time_allotted: str
    difficulty: int
    priority: int
    subject_id: int
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[AiTaskResponse])
def list_ai_tasks():
    """List all AI tasks."""
    with get_session() as session:
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session)
        )
        return service.list_all()


@router.post("/", response_model=AiTaskResponse, status_code=status.HTTP_201_CREATED)
def add_ai_task(payload: AiTaskCreateRequest):
    """Add a new AI task."""
    with get_session() as session:
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session)
        )
        try:
            task = service.create_task(
                ai_task_name=payload.ai_task_name,
                time_allotted=payload.time_allotted,
                difficulty=payload.difficulty,
                priority=payload.priority,
                subject_id=payload.subject_id,
            )
            return task
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")


@router.get("/{task_id}", response_model=AiTaskResponse)
def get_ai_task(task_id: int):
    """Get a specific AI task."""
    with get_session() as session:
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session)
        )
        task = service.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task


@router.patch("/{task_id}", response_model=AiTaskResponse)
def update_ai_task(task_id: int, payload: AiTaskUpdateRequest):
    """Update an AI task."""
    with get_session() as session:
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session)
        )
        try:
            task = service.update_task(
                task_id=task_id,
                ai_task_name=payload.ai_task_name,
                time_allotted=payload.time_allotted,
                difficulty=payload.difficulty,
                priority=payload.priority,
                subject_id=payload.subject_id,
            )
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return task
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ai_task(task_id: int):
    """Delete an AI task."""
    with get_session() as session:
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session)
        )
        if not service.delete_task(task_id):
            raise HTTPException(status_code=404, detail="Task not found")


@router.get("/subject/{subject_id}", response_model=List[AiTaskResponse])
def list_tasks_for_subject(subject_id: int):
    """List all tasks for a specific subject."""
    with get_session() as session:
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session)
        )
        return service.list_for_subject(subject_id)


@router.get("/priority/{priority}", response_model=List[AiTaskResponse])
def list_tasks_by_priority(priority: int):
    """List tasks by priority."""
    with get_session() as session:
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session)
        )
        try:
            return service.list_by_priority(priority)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.get("/difficulty/{difficulty}", response_model=List[AiTaskResponse])
def list_tasks_by_difficulty(difficulty: int):
    """List tasks by difficulty."""
    with get_session() as session:
        service = AITaskService(
            AITaskRepository(session),
            SubjectRepository(session)
        )
        try:
            return service.list_by_difficulty(difficulty)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))