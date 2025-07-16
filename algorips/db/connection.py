from __future__ import annotations

import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    """Return a SQLAlchemy engine connected to MySQL."""
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "example")
    host = os.getenv("MYSQL_HOST", "localhost")
    database = os.getenv("MYSQL_DATABASE", "algorips")
    url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    engine = create_engine(url, future=True)
    return engine
