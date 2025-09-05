from sqlalchemy.orm import Session
from app.models.building import Building


class BuildingRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0):
        return self.db.query(Building).offset(offset).limit(limit).all()
