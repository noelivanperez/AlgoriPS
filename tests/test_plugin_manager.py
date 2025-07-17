from pathlib import Path
import logging

from algorips.core.plugins.manager import PluginManager
from algorips.core.plugins.contract import BasePlugin
from importlib import metadata


class DummyPlugin(BasePlugin):
    def name(self) -> str:
        return "dummy"

    def version(self) -> str:
        return "0.1"

    def register(self, cli, gui_registry) -> None:
        if cli is not None:
            cli.called = True
        if gui_registry is not None:
            gui_registry.append("dummy")

    @property
    def description(self) -> str:
        return "Dummy plugin"

    @property
    def dependencies(self) -> list[str]:
        return []


class MissingRegisterPlugin:
    def name(self) -> str:
        return "bad"

    def version(self) -> str:
        return "0.1"


class FailingRegisterPlugin(BasePlugin):
    def name(self) -> str:
        return "failreg"

    def version(self) -> str:
        return "0.1"

    def register(self, cli, gui_registry) -> None:
        raise RuntimeError("boom")


def create_plugin(path: Path) -> None:
    create_custom_plugin(path, "dummy", "DummyPlugin")


def create_custom_plugin(path: Path, pkg_name: str, cls_name: str) -> None:
    pkg = path / pkg_name
    pkg.mkdir(parents=True, exist_ok=True)
    init = pkg / "__init__.py"
    init.write_text(f"from tests.test_plugin_manager import {cls_name} as Plugin\n")


def test_discover(tmp_path: Path):
    create_plugin(tmp_path)
    mgr = PluginManager(plugin_dir=tmp_path)
    plugins = mgr.discover()
    assert "dummy" in plugins


def test_activate_deactivate(tmp_path: Path):
    create_plugin(tmp_path)
    cli = type("CLI", (), {})()
    gui = []
    mgr = PluginManager(cli=cli, gui_registry=gui, plugin_dir=tmp_path)
    mgr.discover()
    mgr.activate("dummy")
    assert "dummy" in mgr._active
    assert getattr(cli, "called", False) is True
    assert gui == ["dummy"]
    mgr.deactivate("dummy")
    assert "dummy" not in mgr._active


def test_install_uninstall(tmp_path: Path):
    plugin_src = tmp_path / "src"
    create_plugin(plugin_src)
    plugin_dir = tmp_path / "plugins"
    mgr = PluginManager(plugin_dir=plugin_dir)
    mgr.install(plugin_src)
    assert (plugin_dir / "src").exists()
    mgr.uninstall("src")
    assert not (plugin_dir / "src").exists()


def test_list_metadata(tmp_path: Path):
    create_plugin(tmp_path)
    mgr = PluginManager(plugin_dir=tmp_path)
    mgr.discover()
    info = next(iter(mgr.list_plugins()))
    assert info["description"] == "Dummy plugin"
    assert info["dependencies"] == []


def test_persistent_activation(tmp_path: Path):
    create_plugin(tmp_path)
    mgr = PluginManager(plugin_dir=tmp_path)
    mgr.discover()
    mgr.activate("dummy")
    assert (tmp_path / "active.json").exists()
    mgr2 = PluginManager(plugin_dir=tmp_path)
    assert "dummy" in mgr2._active


def test_entry_point_loading(tmp_path: Path, monkeypatch):
    class EP:
        def load(self):
            return DummyPlugin

    class EPS(list):
        def select(self, **kwargs):
            if kwargs.get("group") == "algorips.plugins":
                return [EP()]
            return []

    monkeypatch.setattr(metadata, "entry_points", lambda: EPS())
    mgr = PluginManager(plugin_dir=tmp_path)
    plugins = mgr.discover()
    assert "dummy" in plugins


def test_missing_methods(tmp_path: Path, caplog):
    create_custom_plugin(tmp_path, "bad", "MissingRegisterPlugin")
    mgr = PluginManager(plugin_dir=tmp_path)
    with caplog.at_level(logging.WARNING):
        plugins = mgr.discover()
        assert "bad" not in plugins
    assert "missing required methods" in caplog.text


def test_register_failure(tmp_path: Path, caplog):
    create_custom_plugin(tmp_path, "failreg", "FailingRegisterPlugin")
    mgr = PluginManager(plugin_dir=tmp_path)
    mgr.discover()
    with caplog.at_level(logging.WARNING):
        mgr.activate("failreg")
        assert "failreg" not in mgr._active
    assert "failed to register" in caplog.text
