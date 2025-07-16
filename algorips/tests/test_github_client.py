from algorips.core.git.github import GitHubClient


def test_create_pull_request(monkeypatch):
    calls = []

    def fake_post(url, json=None, headers=None):
        calls.append((url, json))
        class Resp:
            def raise_for_status(self):
                pass
            def json(self):
                return {"number": 1}
        return Resp()

    monkeypatch.setattr('requests.post', fake_post)
    client = GitHubClient('token')
    pr = client.create_pull_request('owner', 'repo', 'head', 'base', 'title', 'body', ['rev'], ['label'])
    assert pr['number'] == 1
    assert len(calls) == 3


def test_list_pull_requests(monkeypatch):
    def fake_get(url, headers=None):
        class Resp:
            def raise_for_status(self):
                pass
            def json(self):
                return [{'number': 1}]
        return Resp()
    import requests
    monkeypatch.setattr(requests, 'get', fake_get, raising=False)
    client = GitHubClient('t')
    prs = client.list_pull_requests('o', 'r', 'all')
    assert prs == [{'number': 1}]


def test_merge_pull_request(monkeypatch):
    def fake_put(url, headers=None):
        class Resp:
            def raise_for_status(self):
                pass
            def json(self):
                return {'merged': True}
        return Resp()
    import requests
    monkeypatch.setattr(requests, 'put', fake_put, raising=False)
    client = GitHubClient('t')
    result = client.merge_pull_request('o', 'r', 1)
    assert result['merged'] is True
