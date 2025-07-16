from algorips.core.ollama_client import OllamaClient


def test_ollama_connection(monkeypatch):
    calls = {}

    def fake_post(url, json):
        calls['url'] = url
        calls['json'] = json

        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {'status': 'ok'}

        return FakeResponse()

    monkeypatch.setattr('requests.post', fake_post)

    client = OllamaClient('localhost', 8000)
    result = client.send_prompt('hello')

    assert result == {'status': 'ok'}
    assert calls['url'].endswith('/v1/completions')
    assert calls['json'] == {'prompt': 'hello'}
