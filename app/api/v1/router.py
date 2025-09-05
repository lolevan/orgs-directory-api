from fastapi import APIRouter
from .endpoints import buildings, organizations, search

api_router = APIRouter()
api_router.include_router(buildings.router, prefix="/buildings", tags=["buildings"])
api_router.include_router(
    organizations.router, prefix="/organizations", tags=["organizations"]
)
api_router.include_router(search.router, prefix="/search", tags=["search"])
