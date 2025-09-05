from pydantic import BaseModel, Field


class OrmBase(BaseModel):
    class Config:
        from_attributes = True


class Pagination(BaseModel):
    limit: int = Field(ge=1, le=100, default=20)
    offset: int = Field(ge=0, default=0)
