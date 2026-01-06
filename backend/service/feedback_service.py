from __future__ import annotations
from typing import List, Optional

from backend.domain.feedback import Feedback
from backend.repository.feedback_repository import FeedbackRepository
from backend.repository.user_repository import UserRepository
from backend.repository.plan_repository import PlanRepository


class FeedbackService:
    def __init__(
        self,
        feedback_repo: FeedbackRepository,
        user_repo: UserRepository,
        plan_repo: PlanRepository,
    ):
        self.feedback_repo = feedback_repo
        self.user_repo = user_repo
        self.plan_repo = plan_repo

    def create_feedback(
        self,
        *,
        user_id: int,
        generation_id: Optional[str] = None,
        plan_id: Optional[int] = None,
        rating: int,
        comments: Optional[str] = None,
    ) -> Feedback:
        """
        Create feedback for a schedule/generation.
        Can accept either generation_id directly or plan_id (will look up generation_id).
        """
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        if not self.user_repo.get(user_id):
            raise ValueError("User does not exist")

        # Resolve generation_id from plan_id if not provided
        if not generation_id and plan_id:
            plan = self.plan_repo.get(plan_id)
            if not plan:
                raise ValueError("Plan does not exist")
            if plan.user_id != user_id:
                raise ValueError("Plan does not belong to this user")
            generation_id = plan.generation_id
            if not generation_id:
                raise ValueError("Plan does not have a generation_id")
        elif not generation_id:
            raise ValueError("Either generation_id or plan_id must be provided")

        # Check if feedback already exists for this generation
        existing = self.feedback_repo.get_by_generation(user_id, generation_id)
        if existing:
            raise ValueError("Feedback already exists for this schedule")

        feedback = Feedback()
        feedback.user_id = user_id
        feedback.generation_id = generation_id
        feedback.rating = rating
        feedback.comments = comments
        
        self.feedback_repo.add(feedback)
        return feedback

    def update_feedback(
        self,
        *,
        user_id: int,
        generation_id: str,
        rating: Optional[int] = None,
        comments: Optional[str] = None,
    ) -> Feedback:
        """Update feedback for a schedule/generation."""
        feedback = self.feedback_repo.get_by_generation(user_id, generation_id)
        if not feedback:
            raise ValueError("Feedback not found for this schedule")

        if rating is not None:
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")
            feedback.rating = rating

        if comments is not None:
            feedback.comments = comments

        return feedback

    def list_feedback_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Feedback]:
        return self.feedback_repo.list_for_user(user_id, offset=offset, limit=limit)

    def get_latest_feedback_for_user(self, user_id: int, limit: int = 2) -> List[Feedback]:
        return self.feedback_repo.list_for_user(user_id, offset=0, limit=limit)

    def get_feedback_for_generation(self, user_id: int, generation_id: str) -> Optional[Feedback]:
        """Get feedback for a specific generation."""
        return self.feedback_repo.get_by_generation(user_id, generation_id)