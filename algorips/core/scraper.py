"""Simple web scraper for AlgoriPS."""

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List

from urllib import request

try:  # optional dependency
    import requests as _requests  # type: ignore
except Exception:  # pragma: no cover - not installed
    _requests = None


@dataclass
class ScrapeTarget:
    """Single URL target and associated CSS selectors."""

    url: str
    selectors: Dict[str, str]


@dataclass
class ScrapeConfig:
    """Configuration parsed from YAML."""

    targets: List[ScrapeTarget]


def _simple_yaml_load(text: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    i = 0
    while i < len(lines):
        line = lines[i].lstrip()
        if line.startswith("targets:"):
            i += 1
            targets = []
            while i < len(lines) and lines[i].lstrip().startswith("- "):
                t: Dict[str, Any] = {}
                if lines[i].lstrip().startswith("- url:"):
                    t["url"] = lines[i].split(":", 1)[1].strip()
                    i += 1
                if i < len(lines) and lines[i].lstrip() == "selectors:":
                    i += 1
                    selectors = {}
                    while i < len(lines) and lines[i].startswith(" " * 6):
                        key, val = lines[i].strip().split(":", 1)
                        selectors[key.strip()] = val.strip()
                        i += 1
                    t["selectors"] = selectors
                targets.append(t)
            data["targets"] = targets
        else:
            i += 1
    return data


def load_config(path: str | Path) -> ScrapeConfig:
    """Load YAML configuration from *path* without external dependencies."""

    text = Path(path).read_text()
    try:  # Use PyYAML if available
        import yaml as _yaml  # type: ignore

        data = _yaml.safe_load(text)
    except Exception:  # pragma: no cover - fallback parser
        data = _simple_yaml_load(text)
    targets = [
        ScrapeTarget(t["url"], t.get("selectors", {})) for t in data.get("targets", [])
    ]
    return ScrapeConfig(targets)


class WebScraper:
    """Fetch pages and extract data according to configuration."""

    def __init__(self, config: ScrapeConfig) -> None:
        self.config = config

    def fetch(self, url: str) -> str:
        if _requests and hasattr(_requests, "get"):
            resp = _requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp.text
        with request.urlopen(url, timeout=10) as resp:
            return resp.read().decode()

    def scrape_target(self, target: ScrapeTarget) -> Dict[str, Any]:
        html = self.fetch(target.url)

        def extract(selector: str) -> str | None:
            class Parser(HTMLParser):
                def __init__(self) -> None:
                    super().__init__()
                    self.capture = False
                    self.text_parts: List[str] = []

                def handle_starttag(self, tag, attrs):
                    cls = None
                    for n, v in attrs:
                        if n == "class":
                            cls = v
                    if "." in selector:
                        sel_tag, sel_cls = selector.split(".", 1)
                    else:
                        sel_tag, sel_cls = selector, None
                    if tag == sel_tag and (sel_cls is None or (cls and sel_cls in cls.split())):
                        self.capture = True

                def handle_endtag(self, tag):
                    if self.capture and tag == selector.split(".")[0]:
                        self.capture = False

                def handle_data(self, data):
                    if self.capture:
                        self.text_parts.append(data)

            p = Parser()
            p.feed(html)
            text = "".join(p.text_parts).strip()
            return text or None

        data = {name: extract(sel) for name, sel in target.selectors.items()}
        return {"url": target.url, "data": data}

    def scrape(self) -> List[Dict[str, Any]]:
        results = []
        for target in self.config.targets:
            results.append(self.scrape_target(target))
        return results
