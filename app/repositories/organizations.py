from typing import Iterable
from sqlalchemy import func, and_
from sqlalchemy.orm import Session, joinedload
from app.models.organization import Organization, organization_activities
from app.models.building import Building


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id_: int) -> Organization | None:
        return (
            self.db.query(Organization)
            .options(
                joinedload(Organization.building),
                joinedload(Organization.phones),
                joinedload(Organization.activities),
            )
            .filter(Organization.id == id_)
            .first()
        )

    def list_by_building(self, building_id: int, limit: int, offset: int):
        q = (
            self.db.query(Organization)
            .options(
                joinedload(Organization.building),
                joinedload(Organization.phones),
                joinedload(Organization.activities),
            )
            .filter(Organization.building_id == building_id)
        )
        return q.offset(offset).limit(limit).all()

    def list_by_activities(self, activity_ids: Iterable[int], limit: int, offset: int):
        q = (
            self.db.query(Organization)
            .join(
                organization_activities,
                Organization.id == organization_activities.c.organization_id,
            )
            .filter(organization_activities.c.activity_id.in_(list(activity_ids)))
            .options(
                joinedload(Organization.building),
                joinedload(Organization.phones),
                joinedload(Organization.activities),
            )
            .distinct()
        )
        return q.offset(offset).limit(limit).all()

    def search_by_name(self, name: str, limit: int, offset: int):
        pattern = f"%{name}%"
        q = (
            self.db.query(Organization)
            .filter(Organization.name.ilike(pattern))
            .options(
                joinedload(Organization.building),
                joinedload(Organization.phones),
                joinedload(Organization.activities),
            )
        )
        return q.offset(offset).limit(limit).all()

    def list_in_bbox(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
        limit: int,
        offset: int,
    ):
        q = (
            self.db.query(Organization)
            .join(Building, Organization.building_id == Building.id)
            .filter(
                and_(
                    Building.latitude >= min_lat,
                    Building.latitude <= max_lat,
                    Building.longitude >= min_lon,
                    Building.longitude <= max_lon,
                )
            )
            .options(
                joinedload(Organization.building),
                joinedload(Organization.phones),
                joinedload(Organization.activities),
            )
        )
        return q.offset(offset).limit(limit).all()

    def list_in_radius(
        self, lat: float, lon: float, radius_km: float, limit: int, offset: int
    ):
        lat_delta = radius_km / 111.0
        lon_delta = radius_km / (111.0 * func.cos(func.radians(lat)))

        bbox_q = (
            self.db.query(Organization.id, Building.latitude, Building.longitude)
            .join(Building, Organization.building_id == Building.id)
            .filter(
                and_(
                    Building.latitude.between(lat - lat_delta, lat + lat_delta),
                    Building.longitude.between(lon - lon_delta, lon + lon_delta),
                )
            )
        ).subquery()

        R = 6371.0
        dist_expr = R * func.acos(
            func.cos(func.radians(lat))
            * func.cos(func.radians(bbox_q.c.latitude))
            * func.cos(func.radians(bbox_q.c.longitude) - func.radians(lon))
            + func.sin(func.radians(lat)) * func.sin(func.radians(bbox_q.c.latitude))
        )

        q = (
            self.db.query(Organization)
            .join(bbox_q, Organization.id == bbox_q.c.id)
            .filter(dist_expr <= radius_km)
            .options(
                joinedload(Organization.building),
                joinedload(Organization.phones),
                joinedload(Organization.activities),
            )
        )
        return q.offset(offset).limit(limit).all()
