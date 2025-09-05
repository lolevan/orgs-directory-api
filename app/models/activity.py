from sqlalchemy import ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="SET NULL")
    )
    depth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    parent: Mapped["Activity"] = relationship(
        "Activity", remote_side=[id], backref="children"
    )

    __table_args__ = (CheckConstraint("depth <= 3", name="ck_activity_depth"),)
