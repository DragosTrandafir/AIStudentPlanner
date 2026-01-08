from __future__ import annotations
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.domain.user import User
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def list_all(self, offset: int = 0, limit: int = 100) -> List[User]:
        stmt = select(User).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.scalar(stmt)

    def get_by_google_id(self, google_id: str) -> Optional[User]:
        stmt = select(User).where(User.google_id == google_id)
        return self.session.scalar(stmt)

    def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        return self.session.scalar(stmt)

    def get_by_username_or_email(self, username_or_email: str) -> Optional[User]:
        stmt = select(User).where(
            (User.username == username_or_email) | (User.email == username_or_email)
        )
        return self.session.scalar(stmt)