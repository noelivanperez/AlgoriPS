import pytest
from sqlalchemy import text

from algorips.core.db import get_engine


@pytest.mark.integration
def test_db_connection(docker_services):
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
