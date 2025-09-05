from sqlalchemy.orm import Session
from app.repositories.activities import ActivityRepository


class ActivityService:
    def __init__(self, db: Session):
        self.repo = ActivityRepository(db)

    def get(self, id_: int):
        return self.repo.get(id_)

    def descendants_ids(self, id_: int):
        return self.repo.descendants_ids(id_)
