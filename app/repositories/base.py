from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get(self, id_: int) -> T | None:
        return self.db.get(self.model, id_)
