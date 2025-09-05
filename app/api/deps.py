from typing import Generator
from fastapi import Depends
from app.core.security import api_key_auth
from app.db.session import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Require API key
def require_api_key(_: None = Depends(api_key_auth)):
    return
