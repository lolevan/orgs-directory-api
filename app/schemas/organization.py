from typing import List
from pydantic import BaseModel
from .common import OrmBase
from .building import BuildingOut
from .activity import ActivityOut


class OrganizationPhoneOut(OrmBase):
    id: int
    phone: str


class OrganizationBase(BaseModel):
    name: str


class OrganizationOut(OrmBase, OrganizationBase):
    id: int
    building: BuildingOut
    phones: List[OrganizationPhoneOut]
    activities: List[ActivityOut]
