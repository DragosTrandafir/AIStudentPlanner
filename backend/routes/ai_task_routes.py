from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.repository.ai_task_repository import AITaskRepository
from backend.repository.subject_repository import SubjectRepository
from backend.repository.project_repository import ProjectRepository
from backend.service.ai_task_service import AITaskService

router = APIRouter(prefix="/ai-task", tags=["ai-task"])

class AiTaskResponseDto(BaseModel):
    id: int
    title: str
    estimated_hours: int
    subject_id: int
    project_id: int 
    status: str 
    scheduled_start: datetime
    scheduled_end: datetime 
    mini_plan: Dict[str, Any] | None
    notes: str

class AiTaskRequestDto(BaseModel):
    title: str
    estimated_hours: int
    subject_id: int
    project_id: int 
    status: str 
    scheduled_start: datetime
    scheduled_end: datetime 
    mini_plan: Dict[str, Any] | None
    notes: str


@router.get("/", response_model=List[AiTaskResponseDto])
def list_aiTask():
    """List all ai_tasks"""
    with get_session() as session:
        subject_repo = SubjectRepository(session)
        project_repo = ProjectRepository(session)
        ai_task_repo = AITaskRepository(session)
        service = AITaskService(ai_task_repo, subject_repo, project_repo)
        return service.list_all()
    
@router.post("/", response_model=AiTaskResponseDto, status_code=status.HTTP_201_CREATED)
def add_aiTask(
    payload: AiTaskRequestDto
):
    """Add a new AiTask to a specific user."""
    with get_session() as session:
        subject_repo = SubjectRepository(session)
        project_repo = ProjectRepository(session)
        ai_task_repo = AITaskRepository(session)
        service = AITaskService(ai_task_repo, subject_repo, project_repo)
        try:
            task=service.create_task(
                title=payload.title,
                estimated_hours=payload.estimated_hours,
                subject_id=payload.subject_id,
                project_id=payload.project_id,
                status=payload.status,
                scheduled_start=payload.scheduled_start,
                scheduled_end=payload.scheduled_end,
                mini_plan=payload.mini_plan,
                notes=payload.notes
            )
            return task
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")