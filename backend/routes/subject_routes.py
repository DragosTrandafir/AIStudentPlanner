from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.domain.enums import SubjectType, SubjectStatus
from backend.repository.subject_repository import SubjectRepository
from backend.repository.user_repository import UserRepository
from backend.service.subject_service import SubjectService

router = APIRouter(prefix="/users/{user_id}/subjects", tags=["subjects"])


class SubjectCreateRequest(BaseModel):
    title: str
    name: str
    type: SubjectType
    status: Optional[SubjectStatus] = None
    difficulty: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None


class SubjectUpdateRequest(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None
    type: Optional[SubjectType] = None
    status: Optional[SubjectStatus] = None
    difficulty: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None


class SubjectResponse(BaseModel):
    id: int
    student_id: int
    title: str
    name: str
    type: SubjectType
    status: SubjectStatus
    difficulty: int
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    description: Optional[str]

    class Config:
        from_attributes = True


@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def add_subject(
    user_id: int,
    payload: SubjectCreateRequest,
):
    """Add a new subject to a specific user."""
    with get_session() as session:
        subject_repo = SubjectRepository(session)
        user_repo = UserRepository(session)
        service = SubjectService(subject_repo, user_repo)
        try:
            subject = service.create_subject(
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
            return subject
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")


@router.get("/", response_model=List[SubjectResponse])
def list_user_subjects(
    user_id: int,
):
    """List all subjects for a specific user."""
    with get_session() as session:
        subject_repo = SubjectRepository(session)
        user_repo = UserRepository(session)
        service = SubjectService(subject_repo, user_repo)
        return service.list_subjects_for_user(user_id)


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(
    user_id: int,
    subject_id: int,
):
    """Get a specific subject for a user."""
    with get_session() as session:
        subject_repo = SubjectRepository(session)
        user_repo = UserRepository(session)
        service = SubjectService(subject_repo, user_repo)
        subject = service.get_subject(subject_id)
        if not subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
        if subject.student_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Subject does not belong to this user")
        return subject


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    user_id: int,
    subject_id: int,
    payload: SubjectUpdateRequest,
):
    """Update a subject for a specific user."""
    with get_session() as session:
        subject_repo = SubjectRepository(session)
        user_repo = UserRepository(session)
        service = SubjectService(subject_repo, user_repo)
        try:
            updated = service.update_subject(
                subject_id=subject_id,
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
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
            return updated
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_subject(
    user_id: int,
    subject_id: int,
):
    """Remove a subject from a specific user."""
    with get_session() as session:
        subject_repo = SubjectRepository(session)
        user_repo = UserRepository(session)
        service = SubjectService(subject_repo, user_repo)
        try:
            success = service.delete_subject(subject_id=subject_id, student_id=user_id)
            if not success:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

