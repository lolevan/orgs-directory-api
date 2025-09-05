from sqlalchemy.orm import Session
from app.repositories.organizations import OrganizationRepository
from app.repositories.activities import ActivityRepository


class OrganizationService:
    def __init__(self, db: Session):
        self.org_repo = OrganizationRepository(db)
        self.act_repo = ActivityRepository(db)

    def get(self, id_: int):
        org = self.org_repo.get(id_)
        if not org:
            from fastapi import HTTPException, status

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
            )
        return org

    def by_building(self, building_id: int, limit: int, offset: int):
        return self.org_repo.list_by_building(building_id, limit, offset)

    def by_activity(
        self, activity_id: int, include_descendants: bool, limit: int, offset: int
    ):
        ids = [activity_id]
        if include_descendants:
            ids = self.act_repo.descendants_ids(activity_id)
            if not ids:
                ids = [activity_id]
        return self.org_repo.list_by_activities(ids, limit, offset)

    def by_activity_name(
        self, name: str, include_descendants: bool, limit: int, offset: int
    ):
        act = self.act_repo.by_name(name)
        if not act:
            from fastapi import HTTPException, status

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found"
            )
        return self.by_activity(act.id, include_descendants, limit, offset)

    def search_by_name(self, name: str, limit: int, offset: int):
        return self.org_repo.search_by_name(name, limit, offset)

    def in_bbox(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
        limit: int,
        offset: int,
    ):
        return self.org_repo.list_in_bbox(
            min_lat, max_lat, min_lon, max_lon, limit, offset
        )

    def in_radius(
        self, lat: float, lon: float, radius_km: float, limit: int, offset: int
    ):
        return self.org_repo.list_in_radius(lat, lon, radius_km, limit, offset)
