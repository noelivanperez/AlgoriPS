"""Utility to execute queries on registered databases."""

from __future__ import annotations

from typing import Any, Dict, List

from sqlalchemy import create_engine, text

from .db import get_engine

# Cache of SQLAlchemy engines per connection name
_engines: dict[str, Any] = {}


def _get_credentials(name: str) -> Dict[str, Any]:
    """Fetch connection credentials from credentials_db."""
    query = text(
        "SELECT host, port, username, password, database_name "
        "FROM credentials_db.db_credentials WHERE name=:name"
    )
    engine = get_engine()
    with engine.connect() as conn:
        row = conn.execute(query, {"name": name}).mappings().first()
        if row is None:
            raise KeyError(name)
        return dict(row)


def _get_engine(name: str) -> Any:
    """Return or create an Engine for the target database."""
    if name not in _engines:
        creds = _get_credentials(name)
        url = (
            f"mysql+pymysql://{creds['username']}:{creds['password']}@"
            f"{creds['host']}:{creds['port']}/{creds['database_name']}"
        )
        _engines[name] = create_engine(url, pool_pre_ping=True, future=True)
    return _engines[name]


def execute_query(name: str, sql: str, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    """Execute SQL on the database referenced by ``name`` and return result rows."""
    engine = _get_engine(name)
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        rows = [dict(row._mapping) for row in result]
    return rows
