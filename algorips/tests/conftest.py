import os
import socket
import time
from urllib.parse import urlparse

import pytest


def _wait_for_port(host: str, port: int, timeout: float = 30.0) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(1)
    return False


@pytest.fixture(scope="session")
def docker_services():
    """Wait for MySQL and Ollama services to be available."""
    mysql_host = os.getenv("MYSQL_HOST", "localhost")
    mysql_port = int(os.getenv("MYSQL_PORT", "3306"))

    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    parsed = urlparse(ollama_url)
    ollama_host = parsed.hostname or "localhost"
    ollama_port = parsed.port or 80

    if not _wait_for_port(mysql_host, mysql_port, timeout=5):
        pytest.skip("MySQL service not available")
    if not _wait_for_port(ollama_host, ollama_port, timeout=5):
        pytest.skip("Ollama service not available")

    yield
