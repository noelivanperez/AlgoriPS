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

try:  # main YAML parser
    import yaml as _yaml  # type: ignore
except Exception:  # pragma: no cover - fallback parser only
    _yaml = None


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
    """Tiny fallback YAML parser.

    Only understands the ``targets`` structure used by the scraper and does not
    support nested mappings or advanced YAML features. Use PyYAML whenever
    possible.
    """

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
    """Load YAML configuration from *path*.

    PyYAML is used when available. If it cannot be imported, a minimal fallback
    parser is used which only understands the ``targets`` list with ``url`` and
    ``selectors``. Nested structures will not be parsed in that mode.
    """

    text = Path(path).read_text()
    if _yaml is not None:
        try:
            data = _yaml.safe_load(text)
        except Exception as exc:  # pragma: no cover - invalid YAML
            raise ValueError(f"Invalid YAML: {exc}") from exc
    else:  # pragma: no cover - fallback parser path
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
                    self.stack: List[tuple[str, List[str]]] = []
                    self.path = [self._split(s) for s in selector.split()]

                @staticmethod
                def _split(token: str) -> tuple[str, str | None]:
                    if "." in token:
                        return token.split(".", 1)[0], token.split(".", 1)[1]
                    return token, None

                def _matches(self) -> bool:
                    if len(self.stack) < len(self.path):
                        return False
                    for (tag, classes), (sel_tag, sel_cls) in zip(
                        self.stack[-len(self.path) :], self.path
                    ):
                        if tag != sel_tag:
                            return False
                        if sel_cls and sel_cls not in classes:
                            return False
                    return True

                def handle_starttag(self, tag, attrs):
                    cls = None
                    for n, v in attrs:
                        if n == "class":
                            cls = v
                    classes = cls.split() if cls else []
                    self.stack.append((tag, classes))
                    if self._matches():
                        self.capture = True

                def handle_endtag(self, tag):
                    if self.capture and len(self.stack) == len(self.path) and tag == self.path[-1][0]:
                        self.capture = False
                    if self.stack:
                        self.stack.pop()

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
