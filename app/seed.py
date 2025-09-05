from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.building import Building
from app.models.activity import Activity
from app.models.organization import Organization, OrganizationPhone


def seed():
    db: Session = SessionLocal()
    try:
        if db.query(Building).first():
            return  # already seeded

        # Buildings
        b1 = Building(
            address="г. Москва, ул. Ленина 1, офис 3",
            latitude=55.7558,
            longitude=37.6173,
        )
        b2 = Building(
            address="г. Москва, пр-т Мира 10", latitude=55.7811, longitude=37.6339
        )
        b3 = Building(
            address="г. Москва, Блюхера 32/1", latitude=55.8000, longitude=37.7000
        )

        db.add_all([b1, b2, b3])

        # Activities:
        # Еда (Мясная продукция, Молочная продукция)
        # Автомобили (Грузовые, Легковые (Запчасти, Аксессуары))
        eat = Activity(name="Еда", parent_id=None, depth=0)
        meat = Activity(name="Мясная продукция", parent=eat, depth=1)
        milk = Activity(name="Молочная продукция", parent=eat, depth=1)

        cars = Activity(name="Автомобили", parent_id=None, depth=0)
        trucks = Activity(name="Грузовые", parent=cars, depth=1)
        cars_light = Activity(name="Легковые", parent=cars, depth=1)
        parts = Activity(name="Запчасти", parent=cars_light, depth=2)
        accessories = Activity(name="Аксессуары", parent=cars_light, depth=2)

        db.add_all([eat, meat, milk, cars, trucks, cars_light, parts, accessories])

        # Organizations
        o1 = Organization(name="ООО Рога и Копыта", building=b3)
        o1.phones = [
            OrganizationPhone(phone="2-222-222"),
            OrganizationPhone(phone="8-923-666-13-13"),
        ]
        o1.activities = [meat, milk]

        o2 = Organization(name="Магазин Запчастей", building=b2)
        o2.phones = [OrganizationPhone(phone="3-333-333")]
        o2.activities = [parts]

        o3 = Organization(name="Молочная ферма", building=b1)
        o3.phones = [OrganizationPhone(phone="+7 495 111 22 33")]
        o3.activities = [milk]

        db.add_all([o1, o2, o3])
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    # Ensure tables exist (alembic should handle migrations; this is a safe-guard)
    Base.metadata.create_all(bind=engine)
    seed()
