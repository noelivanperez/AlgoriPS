"""Utility script to bootstrap the MySQL database."""

import os
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "db" / "migrations"


def get_engine() -> Engine:
    """Return an engine for the target database."""
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "example")
    host = os.getenv("MYSQL_HOST", "localhost")
    database = os.getenv("MYSQL_DATABASE", "algorips")
    url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    return create_engine(url, future=True)


def ensure_database() -> None:
    """Create the database and user if they do not exist."""
    host = os.getenv("MYSQL_HOST", "localhost")
    root_pw = os.getenv("MYSQL_ROOT_PASSWORD", os.getenv("MYSQL_PASSWORD", "example"))
    database = os.getenv("MYSQL_DATABASE", "algorips")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "example")

    root_url = f"mysql+pymysql://root:{root_pw}@{host}/"
    root_engine = create_engine(root_url, future=True)
    with root_engine.begin() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))
        if user != "root":
            conn.execute(
                text(
                    f"CREATE USER IF NOT EXISTS '{user}'@'%' IDENTIFIED BY '{password}'"
                )
            )
            conn.execute(text(f"GRANT ALL PRIVILEGES ON {database}.* TO '{user}'@'%'"))


def run_migrations():
    ensure_database()
    engine = get_engine()
    for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
        stmt = sql_file.read_text()
        with engine.begin() as conn:
            conn.execute(text(stmt))
        print(f"Applied {sql_file.name}")


if __name__ == "__main__":
    run_migrations()
