import threading
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import pytest

from algorips.core.scraper import ScrapeConfig, ScrapeTarget, WebScraper


@pytest.mark.integration
def test_scraper_integration(tmp_path: Path):
    html_file = tmp_path / "index.html"
    html_file.write_text("<html><body><h1>Index</h1></body></html>")

    handler = partial(SimpleHTTPRequestHandler, directory=str(tmp_path))
    server = HTTPServer(("localhost", 0), handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    try:
        url = f"http://localhost:{server.server_address[1]}/index.html"
        cfg = ScrapeConfig([ScrapeTarget(url, {"title": "h1"})])
        result = WebScraper(cfg).scrape()
        assert result == [{"url": url, "data": {"title": "Index"}}]
    finally:
        server.shutdown()
        thread.join()


