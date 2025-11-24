from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.repository.project_repository import ProjectRepository
from backend.repository.user_repository import UserRepository
from backend.service.project_service import ProjectService

router = APIRouter(prefix="/users/{user_id}/projects", tags=["projects"])


class ProjectCreateRequest(BaseModel):
    title: str
    deadline: Optional[datetime] = None
    estimated_effort: Optional[int] = 1
    difficulty: Optional[int] = 1
    description: Optional[str] = None


class ProjectUpdateRequest(BaseModel):
    title: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_effort: Optional[int] = None
    difficulty: Optional[int] = None
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    student_id: int
    title: str
    deadline: Optional[datetime]
    estimated_effort: int
    difficulty: int
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def add_project(
    user_id: int,
    payload: ProjectCreateRequest,
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


@router.get("/", response_model=List[ProjectResponse])
def list_user_projects(
    user_id: int,
):
    """List all projects for a specific user."""
    with get_session() as session:
        project_repo = ProjectRepository(session)
        user_repo = UserRepository(session)
        service = ProjectService(project_repo, user_repo)
        return service.list_projects_for_user(user_id)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    user_id: int,
    project_id: int
):
    """Get a specific project for a user."""
    with get_session() as session:
        project_repo = ProjectRepository(session)
        user_repo = UserRepository(session)
        service = ProjectService(project_repo, user_repo)
        project = service.get_project(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if project.student_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project does not belong to this user")
        return project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    user_id: int,
    project_id: int,
    payload: ProjectUpdateRequest
):
    """Update a project for a specific user."""
    with get_session() as session:
        project_repo = ProjectRepository(session)
        user_repo = UserRepository(session)
        service = ProjectService(project_repo, user_repo)
        try:
            updated = service.update_project(
                project_id=project_id,
                student_id=user_id,
                title=payload.title,
                deadline=payload.deadline,
                estimated_effort=payload.estimated_effort,
                difficulty=payload.difficulty,
                description=payload.description,
            )
            if not updated:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
            return updated
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    user_id: int,
    project_id: int
):
    """Remove a project from a specific user."""
    with get_session() as session:
        project_repo = ProjectRepository(session)
        user_repo = UserRepository(session)
        service = ProjectService(project_repo, user_repo)
        try:
            success = service.delete_project(project_id=project_id, student_id=user_id)
            if not success:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))