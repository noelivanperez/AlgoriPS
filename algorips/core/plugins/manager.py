"""Plugin discovery and management."""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable

from .contract import BasePlugin


class PluginManager:
    """Load and manage AlgoriPS plugins."""

    def __init__(self, cli: Any | None = None, gui_registry: Any | None = None, plugin_dir: str | Path | None = None) -> None:
        root = Path(__file__).resolve().parents[3]
        self.plugin_dir = Path(plugin_dir) if plugin_dir else root / "plugins"
        self.cli = cli
        self.gui_registry = gui_registry
        self._plugins: Dict[str, BasePlugin] = {}
        self._active: set[str] = set()

    def discover(self) -> Dict[str, BasePlugin]:
        """Scan plugin directory and return discovered plugins."""
        self._plugins.clear()
        if not self.plugin_dir.exists():
            return self._plugins
        for path in self.plugin_dir.iterdir():
            if not path.is_dir():
                continue
            init_py = path / "__init__.py"
            if not init_py.exists():
                continue
            mod_name = path.name.replace('-', '_')
            spec = importlib.util.spec_from_file_location(f"plugins.{mod_name}", init_py)
            if not spec or not spec.loader:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore[attr-defined]
            plugin_cls = getattr(module, "Plugin", None)
            if not plugin_cls:
                continue
            plugin: BasePlugin = plugin_cls()
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
                "active": name in self._active,
            }

    def activate(self, name: str) -> None:
        """Activate and register a plugin."""
        if name not in self._plugins:
            self.discover()
        plugin = self._plugins[name]
        plugin.register(self.cli, self.gui_registry)
        self._active.add(name)

    def deactivate(self, name: str) -> None:
        """Deactivate a plugin without removing it."""
        self._active.discard(name)

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
