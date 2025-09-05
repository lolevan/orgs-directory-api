from pydantic import BaseModel, Field
from .common import OrmBase


class ActivityBase(BaseModel):
    name: str
    parent_id: int | None = None
    depth: int = Field(ge=0, le=3, default=0)


class ActivityOut(OrmBase, ActivityBase):
    id: int
