from __future__ import annotations
from typing import List, Optional

from backend.domain.feedback import Feedback
from backend.repository.feedback_repository import FeedbackRepository
from backend.repository.user_repository import UserRepository
from backend.repository.ai_task_repository import AITaskRepository


class FeedbackService:
    def __init__(self, feedback_repo: FeedbackRepository, user_repo: UserRepository, ai_task_repo: AITaskRepository):
        self.feedback_repo = feedback_repo
        self.user_repo = user_repo
        self.ai_task_repo = ai_task_repo

    def create_feedback(
        self,
        *,
        user_id: int,
        rating: int,
        comments: Optional[str] = None,
        ai_task_id: Optional[int] = None,
    ) -> Feedback:
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        if not self.user_repo.get(user_id):
            raise ValueError("User does not exist")
        if ai_task_id is not None and not self.ai_task_repo.get(ai_task_id):
            raise ValueError("AI Task does not exist")

        fb = Feedback(user_id=user_id, ai_task_id=ai_task_id, rating=rating, comments=comments)
        self.feedback_repo.add(fb)
        return fb

    def get_feedback(self, feedback_id: int) -> Optional[Feedback]:
        return self.feedback_repo.get(feedback_id)

    def list_feedback_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Feedback]:
        return self.feedback_repo.list_for_user(user_id, offset=offset, limit=limit)

    def list_feedback_for_task(self, ai_task_id: int, *, offset: int = 0, limit: int = 100) -> List[Feedback]:
        return self.feedback_repo.list_for_task(ai_task_id, offset=offset, limit=limit)
    
    def get_latest_feedback_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Feedback]:
        return self.feedback_repo.get_latest_feedback_by_user(user_id=user_id)
