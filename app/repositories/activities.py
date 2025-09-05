from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models.activity import Activity


class ActivityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id_: int) -> Activity | None:
        return self.db.get(Activity, id_)

    def by_name(self, name: str) -> Activity | None:
        return self.db.query(Activity).filter(Activity.name.ilike(name)).first()

    def descendants_ids(self, root_id: int) -> list[int]:
        # Recursive CTE to get all descendants including the root
        sql = text("""
            WITH RECURSIVE sub(id) AS (
                SELECT id FROM activities WHERE id = :root
                UNION ALL
                SELECT a.id FROM activities a
                JOIN sub s ON a.parent_id = s.id
            )
            SELECT id FROM sub
        """)
        rows = self.db.execute(sql, {"root": root_id}).fetchall()
        return [r[0] for r in rows]
