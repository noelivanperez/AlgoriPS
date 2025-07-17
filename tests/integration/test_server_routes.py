import pytest
from algorips.core.server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.mark.integration
def test_healthz(client):
    resp = client.get('/healthz')
    assert resp.status_code == 200
    assert resp.data == b'ok'


@pytest.mark.integration
def test_metrics(client):
    resp = client.get('/metrics')
    assert resp.status_code == 200
    assert resp.mimetype == 'text/plain'


@pytest.mark.integration
def test_analyze_success(monkeypatch, client, tmp_path):
    expected = {'path': str(tmp_path), 'line_count': 1, 'function_count': 2, 'class_count': 3}

    def fake_scan(path):
        assert path == str(tmp_path)
        return expected

    monkeypatch.setattr('algorips.core.server.CodeAnalyzer.scan', fake_scan)
    resp = client.get('/analyze', query_string={'path': str(tmp_path)})
    assert resp.status_code == 200
    assert resp.get_json() == expected


@pytest.mark.integration
def test_chat_route(monkeypatch, client):
    expected = {'choices': [{'text': 'ok'}]}
    saved = {}

    def fake_send(prompt):
        assert prompt == 'hello'
        return expected

    def fake_save(prompt, response):
        saved['prompt'] = prompt
        saved['response'] = response

    monkeypatch.setattr('algorips.core.server.client.send_prompt', fake_send)
    monkeypatch.setattr('algorips.core.server.save_conversation', fake_save)
    resp = client.post('/chat', json={'prompt': 'hello', 'temperature': 0.5})
    assert resp.status_code == 200
    assert resp.get_json() == expected
    assert saved['prompt'] == 'hello'
    assert saved['response'] == 'ok'


@pytest.mark.integration
def test_db_query_success(monkeypatch, client):
    expected = [{'id': 1}]

    def fake_query(name, sql, params):
        assert name == 'main'
        assert sql == 'SELECT 1'
        assert params == {'a': 2}
        return expected

    monkeypatch.setattr('algorips.core.server.execute_query', fake_query)
    resp = client.post('/db/query', json={'name': 'main', 'sql': 'SELECT 1', 'params': {'a': 2}})
    assert resp.status_code == 200
    assert resp.get_json() == expected


@pytest.mark.integration
def test_db_query_missing(monkeypatch, client):
    resp = client.post('/db/query', json={'name': 'main'})
    assert resp.status_code == 400
    assert resp.get_json() == {'error': 'name and sql required'}


@pytest.mark.integration
def test_history_routes(monkeypatch, client):
    conversations = [
        {'id': 1, 'prompt': 'p', 'response': 'r', 'timestamp': 't'},
    ]

    monkeypatch.setattr('algorips.core.server.list_all', lambda: conversations)
    resp = client.get('/history')
    assert resp.status_code == 200
    assert resp.get_json() == conversations

    deleted = {}

    def fake_delete(cid=None):
        deleted['id'] = cid

    monkeypatch.setattr('algorips.core.server.delete_conversation', fake_delete)
    resp = client.delete('/history/1')
    assert resp.status_code == 200
    assert deleted['id'] == 1
