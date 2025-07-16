import subprocess
from pathlib import Path

from algorips.core.semantic.patcher import Patcher


def test_generate_and_apply_patch(tmp_path):
    repo = tmp_path
    subprocess.run(["git", "init"], cwd=repo, check=True)
    file_path = repo / "example.py"
    file_path.write_text("print('hi')")
    subprocess.run(["git", "add", "example.py"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True)

    patcher = Patcher()
    patch = patcher.generate_patch("F001", str(file_path))
    assert patch
    assert patcher.apply_patch(patch, cwd=str(repo))
    assert file_path.read_text().endswith("\n")
