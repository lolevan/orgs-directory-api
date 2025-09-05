from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_api_key
from app.services.buildings import BuildingService
from app.schemas.building import BuildingOut
from app.schemas.common import Pagination
from typing import List

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.get("/", response_model=List[BuildingOut])
def list_buildings(
    page: Pagination = Depends(),
    db: Session = Depends(get_db),
):
    svc = BuildingService(db)
    return svc.list(limit=page.limit, offset=page.offset)
