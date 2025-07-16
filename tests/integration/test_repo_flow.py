import subprocess
from pathlib import Path

import pytest
from algorips.core.git import local
from algorips.core.git.github import GitHubClient


@pytest.mark.integration
def test_repo_flow(tmp_path, monkeypatch):
    origin = tmp_path / 'origin.git'
    subprocess.run(['git', 'init', '--bare', origin.name], cwd=tmp_path, check=True)

    repo = tmp_path / 'repo'
    local.clone(str(origin), str(repo))
    subprocess.run(['git', 'config', 'user.email', 'a@b.c'], cwd=repo, check=True)
    subprocess.run(['git', 'config', 'user.name', 'Test'], cwd=repo, check=True)

    local.checkout_branch('feature', create=True, cwd=repo)
    f = repo / 'file.txt'
    f.write_text('content')
    local.commit_all('msg', cwd=repo)
    local.push('feature', cwd=repo)

    calls = []

    def fake_post(url, json=None, headers=None):
        calls.append(url)
        class R:
            def raise_for_status(self):
                pass
            def json(self):
                return {'number': 1, 'merged': True}
        return R()

    monkeypatch.setattr('requests.post', fake_post)
    monkeypatch.setattr('requests.put', fake_post, raising=False)

    client = GitHubClient('t')
    pr = client.create_pull_request('o', 'r', 'feature', 'main', 't', 'b', None, None)
    assert pr['number'] == 1
    result = client.merge_pull_request('o', 'r', 1)
    assert result['merged'] is True
    assert calls
