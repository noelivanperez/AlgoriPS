import json
from pathlib import Path
from typing import Any, Dict

CONFIG_DIR = Path.home() / ".algorips"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_CONFIG: Dict[str, Any] = {"model": "llama3"}


def load() -> Dict[str, Any]:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()


def save(cfg: Dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
