"""Minimal SQLAlchemy ORM stub."""

class Session:
    pass


def sessionmaker(bind=None, future=True):
    def _factory():
        return Session()
    return _factory
