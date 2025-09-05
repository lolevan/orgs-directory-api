# Organizations Directory API

FastAPI сервис (слоистая архитектура: **models → repositories → services → API**), Alembic миграции, Docker, статический API‑ключ.

## Запуск (Docker)

```bash
cp .env.example .env  # при желании
docker compose up --build
```

Приложение доступно на: `http://localhost:8000/api/v1/docs`  
Передавайте API‑ключ в заголовке: `X-API-Key: <ваш_ключ>` (по умолчанию `supersecretapikey`).

## Схема БД

- `buildings (id, address, latitude, longitude)`
- `activities (id, name, parent_id, depth<=3)` — adjacency list, ограничение глубины через CHECK.
- `organizations (id, name, building_id)`
- `organization_phones (id, organization_id, phone)`
- `organization_activities (organization_id, activity_id)`

## Эндпоинты (основные)

- `GET /buildings/` — список зданий
- `GET /organizations/{id}` — карточка организации
- `GET /organizations/by-building/{building_id}` — организации в здании
- `GET /organizations/by-activity/{activity_id}?include_descendants=true` — по виду деятельности (с потомками)
- `GET /organizations/search/by-name?q=...` — поиск по названию
- `GET /organizations/nearby?lat=..&lon=..&radius_km=..` — в радиусе от точки (Haversine)
- `GET /organizations/in-bbox?min_lat=..&max_lat=..&min_lon=..&max_lon=..` — в прямоугольнике
- `GET /search/by-activity-name?name=Еда&include_descendants=true` — по имени вида деятельности

## Архитектура

- **models** — ORM модели SQLAlchemy
- **repositories** — узкоспециализированные запросы к БД (включая CTE и Haversine)
- **services** — бизнес‑логика/композиция репозиториев и обработка статусов ошибок
- **api** — FastAPI эндпоинты и зависимости (DB, API‑key)

## Alembic

Первичная миграция: `migrations/versions/0001_init.py`  
Автогенерация включена через `migrations/env.py` (подхватывает `Base.metadata`).

## Тестовые данные

Скрипт `app/seed.py` — создаёт здания, дерево деятельностей (глубина ≤ 3), организации и телефоны.

## Примеры запросов (curl)

```bash
# Список зданий
curl -H "X-API-Key: supersecretapikey" http://localhost:8000/api/v1/buildings/

# Организации в здании
curl -H "X-API-Key: supersecretapikey" http://localhost:8000/api/v1/organizations/by-building/1

# Поиск по названию
curl -H "X-API-Key: supersecretapikey" "http://localhost:8000/api/v1/organizations/search/by-name?q=Молоч"

# По виду деятельности по имени (с потомками)
curl -H "X-API-Key: supersecretapikey" "http://localhost:8000/api/v1/search/by-activity-name?name=Еда"
```

## Примечания по геопоиску

- Радиус: применяется быстрый bbox и формула Haversine на SQL; на проде рационален PostGIS.
- Прямоугольник: фильтр по lat/lon с индексом.

## Дополнительно

- Валидация параметров (границы широты/долготы, пагинация).
- Единообразные ошибки (404 для отсутствующих сущностей, 401 для неверного API‑ключа).
