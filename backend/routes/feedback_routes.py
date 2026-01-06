from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.repository.feedback_repository import FeedbackRepository
from backend.repository.user_repository import UserRepository
from backend.repository.plan_repository import PlanRepository
from backend.service.feedback_service import FeedbackService

router = APIRouter(prefix="/users/{user_id}/feedback", tags=["feedback"])


class FeedbackCreateRequest(BaseModel):
    plan_id: int
    rating: int
    comments: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    rating: int
    comments: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class LastTwoScheduleFeedbackResponse(BaseModel):
    """Feedback from last two schedules."""
    current_feedback: Optional[FeedbackResponse] = None
    last_feedback: Optional[FeedbackResponse] = None


@router.get("/history", response_model=List[FeedbackResponse])
def list_user_feedback(user_id: int):
    """List all feedbacks for a specific user."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        feedback_repo = FeedbackRepository(session)
        plan_repo = PlanRepository(session)
        service = FeedbackService(feedback_repo, user_repo, plan_repo)
        return service.list_feedback_for_user(user_id=user_id)


@router.get("/latest", response_model=List[FeedbackResponse])
def list_user_feedback_latest(user_id: int):
    """Get the last 2 feedbacks for a specific user."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        feedback_repo = FeedbackRepository(session)
        plan_repo = PlanRepository(session)
        service = FeedbackService(feedback_repo, user_repo, plan_repo)

        latest = service.get_latest_feedback_for_user(user_id, limit=2)
        return latest


@router.get("/last-two-schedules", response_model=LastTwoScheduleFeedbackResponse)
def get_last_two_schedule_feedbacks(user_id: int):
    """Get feedback from the last two schedules (generations)."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        feedback_repo = FeedbackRepository(session)
        current_feedback, last_feedback = feedback_repo.get_last_two_generation_feedbacks(user_id)
        
        return LastTwoScheduleFeedbackResponse(
            current_feedback=current_feedback,
            last_feedback=last_feedback
        )


@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def add_feedback(user_id: int, payload: FeedbackCreateRequest):
    """Add a new feedback for a specific plan."""
    with get_session() as session:
        user_repo = UserRepository(session)
        plan_repo = PlanRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if plan exists
        plan = plan_repo.get(payload.plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        # Check if plan belongs to user
        if plan.user_id != user_id:
            raise HTTPException(status_code=403, detail="Plan does not belong to this user")
        
        feedback_repo = FeedbackRepository(session)
        service = FeedbackService(feedback_repo, user_repo, plan_repo)
        try:
            feedback = service.create_feedback(
                user_id=user_id,
                plan_id=payload.plan_id,
                rating=payload.rating, 
                comments=payload.comments
            )
            return feedback
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")