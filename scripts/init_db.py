import os
from pathlib import Path
from sqlalchemy import create_engine, text

MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "db" / "migrations"


def get_engine():
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "example")
    host = os.getenv("MYSQL_HOST", "localhost")
    database = os.getenv("MYSQL_DATABASE", "algorips")
    url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    return create_engine(url, future=True)


def run_migrations():
    engine = get_engine()
    for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
        stmt = sql_file.read_text()
        with engine.begin() as conn:
            conn.execute(text(stmt))
        print(f"Applied {sql_file.name}")


if __name__ == "__main__":
    run_migrations()
