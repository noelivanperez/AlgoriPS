import sys
from pathlib import Path
import time
import types
import pytest

class _CoverageTracer:
    def __init__(self):
        self.files = {}

    def __call__(self, frame, event, arg):
        if event == 'line':
            filename = frame.f_globals.get('__file__')
            if filename and 'algorips' in filename and filename.endswith('.py'):
                self.files.setdefault(filename, set()).add(frame.f_lineno)
        return self

    def start(self):
        sys.settrace(self)

    def stop(self):
        sys.settrace(None)

    def percent(self):
        total = 0
        covered = 0
        for file, lines in self.files.items():
            try:
                with open(file) as f:
                    file_lines = [l for l in f.readlines() if l.strip()]
                total += len(file_lines)
                covered += len(lines)
            except OSError:
                continue
        return 100.0 if total == 0 else 100.0 * covered / total


def pytest_sessionstart(session):
    tracer = _CoverageTracer()
    tracer.start()
    session.config._cov_tracer = tracer


def pytest_sessionfinish(session, exitstatus):
    tracer = getattr(session.config, '_cov_tracer', None)
    if tracer is None:
        return
    tracer.stop()
    percent = tracer.percent()
    print(f'Coverage: {percent:.1f}%')
    if percent < 80.0:
        session.exitstatus = 1


class _SimpleBenchmark:
    def __init__(self):
        self.stats = types.SimpleNamespace(stats={"mean": 0.0})

    def __call__(self, func, *args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        self.stats.stats["mean"] = end - start
        return result


@pytest.fixture
def benchmark():
    return _SimpleBenchmark()
