from sqlalchemy.orm import Session
from app.repositories.buildings import BuildingRepository


class BuildingService:
    def __init__(self, db: Session):
        self.repo = BuildingRepository(db)

    def list(self, limit: int, offset: int):
        return self.repo.list(limit, offset)
