from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_api_key
from app.services.organizations import OrganizationService
from app.schemas.organization import OrganizationOut
from app.schemas.common import Pagination

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.get("/{org_id}", response_model=OrganizationOut)
def get_org(org_id: int, db: Session = Depends(get_db)):
    svc = OrganizationService(db)
    return svc.get(org_id)


@router.get("/by-building/{building_id}", response_model=List[OrganizationOut])
def orgs_by_building(
    building_id: int,
    page: Pagination = Depends(),
    db: Session = Depends(get_db),
):
    svc = OrganizationService(db)
    return svc.by_building(building_id, limit=page.limit, offset=page.offset)


@router.get("/by-activity/{activity_id}", response_model=List[OrganizationOut])
def orgs_by_activity(
    activity_id: int,
    include_descendants: bool = Query(
        True, description="Include all nested activities"
    ),
    page: Pagination = Depends(),
    db: Session = Depends(get_db),
):
    svc = OrganizationService(db)
    return svc.by_activity(
        activity_id, include_descendants, limit=page.limit, offset=page.offset
    )


@router.get("/search/by-name", response_model=List[OrganizationOut])
def search_by_name(
    q: str = Query(..., min_length=1, description="Organization name substring"),
    page: Pagination = Depends(),
    db: Session = Depends(get_db),
):
    svc = OrganizationService(db)
    return svc.search_by_name(q, limit=page.limit, offset=page.offset)


@router.get("/nearby", response_model=List[OrganizationOut])
def orgs_nearby(
    lat: float,
    lon: float,
    radius_km: float = Query(1.0, gt=0),
    page: Pagination = Depends(),
    db: Session = Depends(get_db),
):
    svc = OrganizationService(db)
    return svc.in_radius(lat, lon, radius_km, limit=page.limit, offset=page.offset)


@router.get("/in-bbox", response_model=List[OrganizationOut])
def orgs_in_bbox(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    page: Pagination = Depends(),
    db: Session = Depends(get_db),
):
    svc = OrganizationService(db)
    return svc.in_bbox(
        min_lat, max_lat, min_lon, max_lon, limit=page.limit, offset=page.offset
    )
