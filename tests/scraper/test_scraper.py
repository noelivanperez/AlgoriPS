import json
from pathlib import Path

import pytest

from algorips.core.scraper import ScrapeConfig, ScrapeTarget, WebScraper, load_config


def test_load_config(tmp_path: Path):
    cfg_file = tmp_path / "config.yml"
    cfg_file.write_text(
        """
        targets:
          - url: http://example.com
            selectors:
              title: h1
        """
    )
    cfg = load_config(cfg_file)
    assert len(cfg.targets) == 1
    assert cfg.targets[0].url == "http://example.com"
    assert cfg.targets[0].selectors == {"title": "h1"}


def test_scrape(monkeypatch):
    html = "<html><body><h1>Hello</h1></body></html>"

    def fake_fetch(self, url: str) -> str:  # type: ignore
        return html

    monkeypatch.setattr(WebScraper, "fetch", fake_fetch)
    config = ScrapeConfig([ScrapeTarget("http://example.com", {"title": "h1"})])
    scraper = WebScraper(config)
    result = scraper.scrape()
    assert result == [{"url": "http://example.com", "data": {"title": "Hello"}}]


def test_scrape_nested_selectors(monkeypatch):
    html = "<html><body><div class='wrapper'><h1>Hello</h1></div></body></html>"

    def fake_fetch(self, url: str) -> str:  # type: ignore
        return html

    monkeypatch.setattr(WebScraper, "fetch", fake_fetch)
    config = ScrapeConfig(
        [ScrapeTarget("http://example.com", {"title": "div.wrapper h1"})]
    )
    scraper = WebScraper(config)
    result = scraper.scrape()
    assert result == [
        {"url": "http://example.com", "data": {"title": "Hello"}}
    ]

