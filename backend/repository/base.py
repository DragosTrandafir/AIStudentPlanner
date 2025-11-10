from __future__ import annotations
from typing import Generic, Iterable, List, Optional, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def add(self, entity: T) -> T:
        self.session.add(entity)
        return entity

    def get(self, entity_id: int) -> Optional[T]:
        return self.session.get(self.model, entity_id)

    def list(self, *, offset: int = 0, limit: int = 100) -> List[T]:
        stmt = select(self.model).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def delete(self, entity: T) -> None:
        self.session.delete(entity)

    def add_all(self, entities: Iterable[T]) -> Sequence[T]:
        self.session.add_all(list(entities))
        return entities
