from __future__ import annotations
from typing import Optional, List

from domain.user import User
from repository.user_repository import UserRepository


class UserService:
    """Service layer for User operations.

    API layer should only call methods from this service.
    """

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, *, name: str, email: str, major: Optional[str] = None, google_id: Optional[str] = None) -> User:
        if not name or not name.strip():
            raise ValueError("Name is required")
        if not email or not email.strip():
            raise ValueError("Email is required")

        # enforce unique email and google_id at service level (db also enforces)
        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("A user with this email already exists")
        if google_id:
            existing_google = self.user_repo.get_by_google_id(google_id)
            if existing_google:
                raise ValueError("A user with this Google ID already exists")

        user = User(name=name.strip(), email=email.strip(), major=major, google_id=google_id)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repo.get(user_id)

    def get_all_users(self) -> List[User]:
        return self.user_repo.list()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_by_email(email)

    def get_by_google_id(self, google_id: str) -> Optional[User]:
        return self.user_repo.get_by_google_id(google_id)
