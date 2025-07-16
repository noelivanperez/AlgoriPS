from pathlib import Path
from locust import User, task, between

from algorips.core.analyzer import CodeAnalyzer

DATA_DIR = Path(__file__).parent / "data"
SMALL_REPO = DATA_DIR / "small_repo"
LARGE_REPO = DATA_DIR / "large_repo"

class ScanSmallRepo(User):
    weight = 1
    wait_time = between(0.5, 1.5)

    def on_start(self):
        self.analyzer = CodeAnalyzer()

    @task
    def scan(self):
        self.analyzer.scan(str(SMALL_REPO))

class ScanLargeRepo(User):
    weight = 5
    wait_time = between(0.5, 1.5)

    def on_start(self):
        self.analyzer = CodeAnalyzer()

    @task
    def scan(self):
        self.analyzer.scan(str(LARGE_REPO))
