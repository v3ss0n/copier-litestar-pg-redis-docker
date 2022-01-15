from typing import Generator
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.core.config import settings

engine = create_engine(settings.DATABASE_URI, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
