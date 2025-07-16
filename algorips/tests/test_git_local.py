import subprocess
from pathlib import Path

from algorips.core.git import local


def _init_repo(path: Path) -> None:
    subprocess.run(["git", "init", "-b", "main"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "you@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "You"], cwd=path, check=True)


def test_clone(tmp_path):
    src = tmp_path / "src"
    dest = tmp_path / "dest"
    src.mkdir()
    _init_repo(src)
    (src / "file.txt").write_text("content")
    local.commit_all("init", cwd=src)

    cloned = local.clone(str(src), str(dest))
    assert (cloned / "file.txt").exists()


def test_checkout_branch(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    (repo / "a.txt").write_text("a")
    local.commit_all("init", cwd=repo)

    local.checkout_branch("feature", create=True, cwd=repo)
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo, check=True, capture_output=True, text=True)
    assert result.stdout.strip() == "feature"


def test_commit_all(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    (repo / "b.txt").write_text("b")
    local.commit_all("first", cwd=repo)
    msg = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()
    assert msg == "first"


def test_push(tmp_path):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", remote.name], cwd=tmp_path, check=True)

    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=repo, check=True)
    (repo / "c.txt").write_text("c")
    local.commit_all("c", cwd=repo)

    local.push("main", cwd=repo)
    result = subprocess.run(["git", "rev-list", "--count", "main"], cwd=remote, check=True, capture_output=True, text=True)
    assert result.stdout.strip() == "1"
