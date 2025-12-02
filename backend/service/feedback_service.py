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
        plan_id: int,
        rating: int,
        comments: Optional[str] = None,
    ) -> Feedback:
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        if not self.user_repo.get(user_id):
            raise ValueError("User does not exist")

        if not self.plan_repo.get(plan_id):
            raise ValueError("Plan does not exist")

        # Check if feedback already exists for this plan
        existing = self.feedback_repo.get_by_plan(plan_id)
        if existing:
            raise ValueError("Feedback already exists for this plan")

        feedback = Feedback()
        feedback.user_id = user_id
        feedback.plan_id = plan_id
        feedback.rating = rating
        feedback.comments = comments
        
        self.feedback_repo.add(feedback)
        return feedback

    def list_feedback_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Feedback]:
        return self.feedback_repo.list_for_user(user_id, offset=offset, limit=limit)

    def get_latest_feedback_for_user(self, user_id: int, limit: int = 2) -> List[Feedback]:
        return self.feedback_repo.list_for_user(user_id, offset=0, limit=limit)