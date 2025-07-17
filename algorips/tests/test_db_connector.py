from algorips.core import db_connector as dc


class DummyRow:
    def __init__(self, mapping):
        self._mapping = mapping


class DummyResult:
    def __init__(self, rows):
        self.rows = [DummyRow(r) for r in rows]

    def mappings(self):
        return self

    def first(self):
        return self.rows[0]._mapping if self.rows else None

    def __iter__(self):
        return iter(self.rows)


class DummyConn:
    def __init__(self, responses):
        self.responses = responses
        self.executed = []

    def execute(self, stmt, params=None):
        self.executed.append((str(stmt), params))
        if 'FROM credentials_db.db_credentials' in str(stmt):
            return self.responses['credentials']
        return self.responses['query']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


class DummyEngine:
    def __init__(self, conn):
        self.conn = conn

    def connect(self):
        return self.conn


def test_execute_query(monkeypatch):
    cred_result = DummyResult([
        {
            'host': 'h',
            'port': 3306,
            'username': 'u',
            'password': 'p',
            'database_name': 'db',
        }
    ])
    query_result = DummyResult([{'a': 1}])

    cred_conn = DummyConn({'credentials': cred_result, 'query': query_result})
    query_conn = DummyConn({'credentials': cred_result, 'query': query_result})

    monkeypatch.setattr(dc, 'get_engine', lambda: DummyEngine(cred_conn))
    monkeypatch.setattr(dc, 'create_engine', lambda url, **kw: DummyEngine(query_conn))

    rows = dc.execute_query('name', 'select * from t', {})

    assert rows == [{'a': 1}]
    assert cred_conn.executed[0][0].startswith('SELECT host')
    assert query_conn.executed[0][0].startswith('select *')
