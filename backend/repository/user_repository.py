from __future__ import annotations
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.domain.user import User
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.scalars(stmt).first()

    def get_by_google_id(self, google_id: str) -> Optional[User]:
        stmt = select(User).where(User.google_id == google_id)
        return self.session.scalars(stmt).first()

