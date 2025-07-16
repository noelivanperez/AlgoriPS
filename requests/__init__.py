"""Minimal requests stub used for offline testing."""

class Response:
    def __init__(self, json_data=None, status_code=200):
        self._json = json_data or {}
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

    def json(self):
        return self._json

def post(url, json=None, **kwargs):
    raise RuntimeError("requests package not available in this environment")
