from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_api_key
from app.services.organizations import OrganizationService
from app.schemas.organization import OrganizationOut
from app.schemas.common import Pagination

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.get("/by-activity-name", response_model=List[OrganizationOut])
def search_by_activity_name(
    name: str = Query(..., min_length=1),
    include_descendants: bool = Query(True),
    page: Pagination = Depends(),
    db: Session = Depends(get_db),
):
    svc = OrganizationService(db)
    return svc.by_activity_name(
        name, include_descendants, limit=page.limit, offset=page.offset
    )
