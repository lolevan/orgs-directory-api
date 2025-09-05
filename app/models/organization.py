from sqlalchemy import Integer, String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False
    )

    building = relationship("Building", back_populates="organizations")
    phones = relationship(
        "OrganizationPhone", cascade="all, delete-orphan", back_populates="organization"
    )
    activities = relationship(
        "Activity", secondary="organization_activities", backref="organizations"
    )


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    phone: Mapped[str] = mapped_column(String(50), nullable=False)

    organization = relationship("Organization", back_populates="phones")


# Association table for M2M
organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column(
        "organization_id",
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "activity_id", ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True
    ),
)
