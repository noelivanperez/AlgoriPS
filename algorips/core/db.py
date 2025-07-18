from __future__ import annotations

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


_engine = None
_SessionLocal = None


def get_engine():
    """Return a SQLAlchemy engine using environment variables."""
    global _engine
    if _engine is None:
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD", "example")
        host = os.getenv("MYSQL_HOST", "localhost")
        database = os.getenv("MYSQL_DATABASE", "algorips")
        pool_size = int(os.getenv("MYSQL_POOL_SIZE", "5"))
        pool_timeout = int(os.getenv("MYSQL_POOL_TIMEOUT", "30"))
        url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
        _engine = create_engine(
            url,
            pool_pre_ping=True,
            pool_size=pool_size,
            pool_timeout=pool_timeout,
            future=True,
        )
    return _engine


def get_session() -> Session:
    """Return a new SQLAlchemy session."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), future=True)
    return _SessionLocal()
