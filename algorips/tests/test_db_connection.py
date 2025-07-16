import pytest
from sqlalchemy import text

from algorips.core.db import get_engine, get_session


@pytest.mark.integration
def test_db_connection(docker_services):
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_get_session_returns_session():
    session = get_session()
    assert session.__class__.__name__ == 'Session'
