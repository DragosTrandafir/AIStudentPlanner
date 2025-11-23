from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.domain.enums import SubjectType, SubjectStatus
from backend.repository.ai_task_repository import AITaskRepository
from backend.repository.project_repository import ProjectRepository
from backend.repository.feedback_repository import FeedbackRepository
from backend.repository.user_repository import UserRepository
from backend.service.project_service import ProjectService

router = APIRouter(prefix="/users/{user_id}/project", tags=["project"])

class ProjectRequestDto(BaseModel):
    title: str
    deadline: datetime
    estimated_effort:int 
    difficulty: int
    description: str

class ProjectResponseDto(BaseModel):
    id:int
    title: str
    deadline: datetime
    estimated_effort:int 
    difficulty: int
    description: str


@router.get("/", response_model=List[ProjectResponseDto])
def list_user_feedback(
    user_id: int,
):
    """List all projects for a specific user."""
    with get_session() as session:
        project_repo = ProjectRepository(session)
        user_repo = UserRepository(session)
        service = ProjectService(project_repo, user_repo)
        return service.list_projects_for_user(user_id)
    
@router.post("/", response_model=ProjectResponseDto, status_code=status.HTTP_201_CREATED)
def add_subject(
    user_id: int,
    payload: ProjectRequestDto,
):
    """Add a new project to a specific user."""
    with get_session() as session:
        project_repo = ProjectRepository(session)
        user_repo = UserRepository(session)
        service = ProjectService(project_repo, user_repo)
        try:
            project=service.create_project(
                student_id=user_id, 
                title=payload.title, 
                deadline=payload.deadline, 
                estimated_effort=payload.estimated_effort,
                difficulty=payload.difficulty, 
                description=payload.description
            )
            return project
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")