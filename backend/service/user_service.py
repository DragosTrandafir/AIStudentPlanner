from __future__ import annotations
from typing import Optional, List

from backend.domain.user import User
from backend.repository.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(
        self,
        *,
        name: str,
        username: str,
        email: str,
        password: str,
        major: Optional[str] = None,
        google_id: Optional[str] = None
    ) -> User:
        if not name or not name.strip():
            raise ValueError("Name is required")
        if not email or not email.strip():
            raise ValueError("Email is required")

        # Enforce unique email and google_id at service level (db also enforces)
        if self.user_repo.get_by_email(email):
            raise ValueError("A user with this email already exists")
        if self.user_repo.get_by_username(username):
            raise ValueError("A user with this username already exists")
        if google_id:
            existing_google = self.user_repo.get_by_google_id(google_id)
            if existing_google:
                raise ValueError("A user with this Google ID already exists")

        user = User()
        user.name = name.strip()
        user.username = username.strip()
        user.email = email.strip()
        user.password = password.strip()
        user.major = major.strip() if major else None
        user.google_id = google_id

        self.user_repo.add(user)
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repo.get(user_id)

    def list_all(self, offset: int = 0, limit: int = 100) -> List[User]:
        return self.user_repo.list_all(offset, limit)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_by_email(email)

    def get_by_google_id(self, google_id: str) -> Optional[User]:
        return self.user_repo.get_by_google_id(google_id)

    def update_user(
        self,
        *,
        user_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        major: Optional[str] = None,
        google_id: Optional[str] = None,
    ) -> Optional[User]:
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if name is not None:
            if not name.strip():
                raise ValueError("Name cannot be empty")
            user.name = name.strip()

        if email is not None:
            if not email.strip():
                raise ValueError("Email cannot be empty")
            # Check if email is already taken by another user
            existing = self.user_repo.get_by_email(email)
            if existing and existing.id != user_id:
                raise ValueError("A user with this email already exists")
            user.email = email.strip()

        if major is not None:
            user.major = major.strip() if major else None

        if google_id is not None:
            # Check if google_id is already taken by another user
            if google_id:
                existing_google = self.user_repo.get_by_google_id(google_id)
                if existing_google and existing_google.id != user_id:
                    raise ValueError("A user with this Google ID already exists")
            user.google_id = google_id

        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.user_repo.get(user_id)
        if not user:
            return False

        self.user_repo.delete(user)
        return True

    def login_user(self, username_or_email: str, password: str) -> User:
        if not username_or_email.strip() or not password.strip():
            raise ValueError("Username/email and password are required")

        user = self.user_repo.get_by_username_or_email(username_or_email.strip())
        if not user:
            raise ValueError("User not found")

        if user.password != password.strip():  # plain text check
            raise ValueError("Incorrect password")

        return user