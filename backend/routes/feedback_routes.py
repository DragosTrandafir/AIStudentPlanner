from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.domain.enums import SubjectType, SubjectStatus
from backend.repository.ai_task_repository import AITaskRepository
from backend.repository.feedback_repository import FeedbackRepository
from backend.repository.user_repository import UserRepository
from backend.service.feedback_service import FeedbackService

router = APIRouter(prefix="/users/{user_id}/feedback", tags=["feedback"])

class FeedbackDto(BaseModel):
    id: int
    user_id: int
    ai_task_id:int
    rating: int
    comments: str



@router.get("/", response_model=List[FeedbackDto])
def list_user_feedback(
    user_id: int,
):
    """List all feedbacks for a specific user."""
    with get_session() as session:
        feedback_repo = FeedbackRepository(session)
        user_repo = UserRepository(session)
        ai_task_repo = AITaskRepository(session)
        service = FeedbackService(feedback_repo, user_repo, ai_task_repo)
        return service.list_feedback_for_user(user_id)
    
@router.post("/", response_model=FeedbackDto, status_code=status.HTTP_201_CREATED)
def add_subject(
    user_id: int,
    payload: FeedbackDto,
):
    """Add a new feedback to a specific user."""
    with get_session() as session:
        feedback_repo = FeedbackRepository(session)
        user_repo = UserRepository(session)
        ai_task_repo = AITaskRepository(session)
        service = FeedbackService(feedback_repo, user_repo, ai_task_repo)
        try:
            service.create_feedback(user_id, payload.rating, payload.comments)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")