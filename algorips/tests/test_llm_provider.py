from algorips.core.llm import OllamaProvider


def test_send_prompt(monkeypatch):
    calls = {}

    def fake_post(url, json=None, timeout=10):
        calls['url'] = url
        calls['json'] = json
        class R:
            def raise_for_status(self):
                pass
            def json(self):
                return {'answer': '42'}
        return R()

    monkeypatch.setattr('requests.post', fake_post)

    provider = OllamaProvider('http://x')

    monkeypatch.setattr(provider, 'list_models', lambda: ['foo'])
    assert provider.model_exists('foo')
    result = provider.send_prompt('hi', 'foo')
    assert result['answer'] == '42'
    assert calls['json']['model'] == 'foo'
