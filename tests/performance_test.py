import time
from pathlib import Path
from algorips.core.analyzer import CodeAnalyzer

def test_large_repo_latency():
    repo = Path('tests/performance/data/large_repo')
    files = list(repo.glob('*.py'))
    start = time.perf_counter()
    CodeAnalyzer().scan(str(repo))
    elapsed = time.perf_counter() - start
    assert elapsed / len(files) <= 0.1, f"Latency {elapsed/len(files):.3f}s > 0.1s per file"
