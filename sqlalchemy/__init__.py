"""Minimal SQLAlchemy stub for offline testing."""

class DummyResult:
    def __init__(self, value=1):
        self._value = value

    def scalar(self):
        return self._value


class DummyConnection:
    def execute(self, *args, **kwargs):
        return DummyResult()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


class DummyEngine:
    def connect(self):
        return DummyConnection()


def create_engine(url, pool_pre_ping=True, future=True):
    return DummyEngine()


def text(sql):
    return sql

