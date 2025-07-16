from pathlib import Path
import subprocess
import pytest

from algorips.core.analyzer import CodeAnalyzer
from algorips.core.semantic.patcher import Patcher

pytest.importorskip("pytest_benchmark")


def _create_repo(path: Path, files: int = 5) -> Path:
    for i in range(files):
        (path / f'f{i}.py').write_text('print("hi")\n')
    return path


def test_analyze_speed(benchmark, tmp_path):
    repo = _create_repo(tmp_path, 5)
    analyzer = CodeAnalyzer()
    result = benchmark(analyzer.scan, str(repo))
    assert result["line_count"] == 5
    assert benchmark.stats.stats["mean"] < 0.2


def test_patch_apply_speed(benchmark, tmp_path):
    repo = tmp_path
    subprocess.run(["git", "init"], cwd=repo, check=True)
    file_path = repo / "example.py"
    file_path.write_text("print('hi')")
    subprocess.run(["git", "add", "example.py"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True)

    patcher = Patcher()
    patch = patcher.generate_patch("F001", str(file_path))

    def run():
        subprocess.run(["git", "reset", "--hard"], cwd=repo, stdout=subprocess.DEVNULL)
        patcher.apply_patch(patch, cwd=str(repo))

    benchmark(run)
    assert benchmark.stats.stats["mean"] < 0.2
