from pydantic import BaseModel, Field
from .common import OrmBase


class BuildingBase(BaseModel):
    address: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class BuildingOut(OrmBase, BuildingBase):
    id: int
