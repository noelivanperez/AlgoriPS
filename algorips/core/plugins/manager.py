"""Plugin discovery and management."""

from __future__ import annotations

import importlib.util
import json
import logging
import shutil
from importlib import metadata
from pathlib import Path
from typing import Any, Dict, Iterable

from .contract import BasePlugin


logger = logging.getLogger(__name__)


class PluginManager:
    """Load and manage AlgoriPS plugins."""

    def __init__(self, cli: Any | None = None, gui_registry: Any | None = None, plugin_dir: str | Path | None = None) -> None:
        root = Path(__file__).resolve().parents[3]
        self.plugin_dir = Path(plugin_dir) if plugin_dir else root / "plugins"
        self.cli = cli
        self.gui_registry = gui_registry
        self._plugins: Dict[str, BasePlugin] = {}
        self._active: set[str] = set()
        self._state_file = self.plugin_dir / "active.json"
        self._load_state()

    # ------------------------------------------------------------------
    # persistence helpers
    # ------------------------------------------------------------------
    def _load_state(self) -> None:
        if self._state_file.exists():
            try:
                data = json.loads(self._state_file.read_text())
                if isinstance(data, list):
                    self._active = set(data)
            except json.JSONDecodeError:
                self._active = set()

    def _save_state(self) -> None:
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        self._state_file.write_text(json.dumps(sorted(self._active)))

    def discover(self) -> Dict[str, BasePlugin]:
        """Scan plugin directory and return discovered plugins."""
        self._plugins.clear()
        if self.plugin_dir.exists():
            for path in self.plugin_dir.iterdir():
                if not path.is_dir():
                    continue
                init_py = path / "__init__.py"
                if not init_py.exists():
                    continue
                mod_name = path.name.replace('-', '_')
                spec = importlib.util.spec_from_file_location(
                    f"plugins.{mod_name}", init_py
                )
                if not spec or not spec.loader:
                    continue
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)  # type: ignore[attr-defined]
                plugin_cls = getattr(module, "Plugin", None)
                if not plugin_cls:
                    continue
                try:
                    plugin: BasePlugin = plugin_cls()
                except TypeError as exc:  # pragma: no cover - invalid plugin
                    logger.warning("Skipping plugin %s: %s", path.name, exc)
                    continue
                if not all(callable(getattr(plugin, m, None)) for m in ("name", "version", "register")):
                    logger.warning(
                        "Skipping plugin %s: missing required methods", path.name
                    )
                    continue
                self._plugins[plugin.name()] = plugin

        for ep in metadata.entry_points().select(group="algorips.plugins"):
            try:
                plugin_cls = ep.load()
            except Exception:  # pragma: no cover - error loading external plugin
                continue
            try:
                plugin = plugin_cls()
            except TypeError as exc:  # pragma: no cover - invalid plugin
                logger.warning("Skipping plugin %s: %s", ep.name, exc)
                continue
            if not all(callable(getattr(plugin, m, None)) for m in ("name", "version", "register")):
                logger.warning(
                    "Skipping plugin %s: missing required methods", ep.name
                )
                continue
            self._plugins[plugin.name()] = plugin
        return self._plugins

    # alias for compatibility
    scan = discover

    def list_plugins(self) -> Iterable[dict[str, Any]]:
        """Return information about available plugins."""
        self.discover()
        for name, plugin in self._plugins.items():
            yield {
                "name": plugin.name(),
                "version": plugin.version(),
                "description": getattr(plugin, "description", ""),
                "dependencies": getattr(plugin, "dependencies", []),
                "active": name in self._active,
            }

    def activate(self, name: str) -> None:
        """Activate and register a plugin."""
        if name not in self._plugins:
            self.discover()
        plugin = self._plugins[name]
        try:
            plugin.register(self.cli, self.gui_registry)
        except Exception as exc:  # pragma: no cover - plugin error
            logger.warning("Plugin %s failed to register: %s", name, exc)
            return
        self._active.add(name)
        self._save_state()

    def deactivate(self, name: str) -> None:
        """Deactivate a plugin without removing it."""
        self._active.discard(name)
        self._save_state()

    def install(self, src: str | Path) -> Path:
        """Install a plugin from a directory or zip archive."""
        src_path = Path(src)
        dest = self.plugin_dir / src_path.name
        if dest.exists():
            raise FileExistsError(dest)
        if src_path.suffix == ".zip":
            shutil.unpack_archive(str(src_path), dest)
        else:
            shutil.copytree(src_path, dest)
        return dest

    def uninstall(self, name: str) -> None:
        """Remove a plugin from disk."""
        path = self.plugin_dir / name
        if path.exists():
            shutil.rmtree(path)
        self._plugins.pop(name, None)
        self._active.discard(name)
        self._save_state()
