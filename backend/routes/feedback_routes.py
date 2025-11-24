from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.repository.ai_task_repository import AITaskRepository
from backend.repository.feedback_repository import FeedbackRepository
from backend.repository.user_repository import UserRepository
from backend.service.feedback_service import FeedbackService

router = APIRouter(prefix="/users/{user_id}/feedback", tags=["feedback"])


class FeedbackCreateRequest(BaseModel):
    ai_task_id: Optional[int] = None
    rating: int
    comments: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    ai_task_id: Optional[int]
    rating: int
    comments: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/history", response_model=List[FeedbackResponse])
def list_user_feedback(
    user_id: int,
):
    """List all feedbacks for a specific user."""
    with get_session() as session:
        feedback_repo = FeedbackRepository(session)
        user_repo = UserRepository(session)
        ai_task_repo = AITaskRepository(session)
        service = FeedbackService(feedback_repo, user_repo, ai_task_repo)
        return service.list_feedback_for_user(user_id=user_id)


@router.get("/latest", response_model=FeedbackResponse)
def list_user_feedback_latest(
    user_id: int,
):
    """List last feedback for a specific user."""
    with get_session() as session:
        feedback_repo = FeedbackRepository(session)
        user_repo = UserRepository(session)
        ai_task_repo = AITaskRepository(session)
        service = FeedbackService(feedback_repo, user_repo, ai_task_repo)

        latest = service.get_latest_feedback_for_user(user_id)
        if not latest:
            raise HTTPException(status_code=404, detail="No feedback found for this user")
        return latest


@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def add_feedback(
    user_id: int,
    payload: FeedbackCreateRequest,
):
    """Add a new feedback to a specific user."""
    with get_session() as session:
        feedback_repo = FeedbackRepository(session)
        user_repo = UserRepository(session)
        ai_task_repo = AITaskRepository(session)
        service = FeedbackService(feedback_repo, user_repo, ai_task_repo)
        try:
            feedback=service.create_feedback(
                user_id=user_id, 
                rating=payload.rating, 
                comments=payload.comments, 
                ai_task_id=payload.ai_task_id
                )
            return feedback
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")