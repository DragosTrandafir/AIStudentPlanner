from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.domain.enums import TaskType, TaskStatus
from backend.repository.task_repository import TaskRepository
from backend.repository.user_repository import UserRepository
from backend.service.task_service import TaskService

router = APIRouter(prefix="/users/{user_id}/tasks", tags=["tasks"])


class TaskCreateRequest(BaseModel):
    title: str
    name: str
    type: TaskType
    status: Optional[TaskStatus] = None
    difficulty: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None
    type: Optional[TaskType] = None
    status: Optional[TaskStatus] = None
    difficulty: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    student_id: int
    title: str
    name: str
    type: TaskType
    status: TaskStatus
    difficulty: int
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    description: Optional[str]

    class Config:
        from_attributes = True


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def add_task(
    user_id: int,
    payload: TaskCreateRequest,
):
    """Add a new task to a specific user."""
    with get_session() as session:
        task_repo = TaskRepository(session)
        user_repo = UserRepository(session)
        service = TaskService(task_repo, user_repo)
        try:
            task = service.create_task(
                student_id=user_id,
                title=payload.title,
                name=payload.name,
                type=payload.type,
                status=payload.status,
                difficulty=payload.difficulty,
                start_date=payload.start_date,
                end_date=payload.end_date,
                description=payload.description,
            )
            return task
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")


@router.get("/", response_model=List[TaskResponse])
def list_user_tasks(
    user_id: int,
):
    """List all tasks for a specific user."""
    with get_session() as session:
        task_repo = TaskRepository(session)
        user_repo = UserRepository(session)
        service = TaskService(task_repo, user_repo)
        return service.list_tasks_for_user(user_id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: int,
    task_id: int,
):
    """Get a specific task for a user."""
    with get_session() as session:
        task_repo = TaskRepository(session)
        user_repo = UserRepository(session)
        service = TaskService(task_repo, user_repo)
        task = service.get_task(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        if task.student_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Task does not belong to this user")
        return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: int,
    task_id: int,
    payload: TaskUpdateRequest,
):
    """Update a task for a specific user."""
    with get_session() as session:
        task_repo = TaskRepository(session)
        user_repo = UserRepository(session)
        service = TaskService(task_repo, user_repo)
        try:
            updated = service.update_task(
                task_id=task_id,
                student_id=user_id,
                title=payload.title,
                name=payload.name,
                type=payload.type,
                status=payload.status,
                difficulty=payload.difficulty,
                start_date=payload.start_date,
                end_date=payload.end_date,
                description=payload.description,
            )
            if not updated:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
            return updated
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(
    user_id: int,
    task_id: int,
):
    """Remove a task from a specific user."""
    with get_session() as session:
        task_repo = TaskRepository(session)
        user_repo = UserRepository(session)
        service = TaskService(task_repo, user_repo)
        try:
            success = service.delete_task(task_id=task_id, student_id=user_id)
            if not success:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

