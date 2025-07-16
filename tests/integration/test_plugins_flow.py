from pathlib import Path

from algorips.core.plugins.manager import PluginManager
from algorips.core.plugins.contract import BasePlugin


class DummyPlugin(BasePlugin):
    def name(self) -> str:
        return "dummy"

    def version(self) -> str:
        return "0.1"

    def register(self, cli, gui_registry) -> None:
        if cli is not None:
            @cli.command("dummy-cmd")
            def _cmd() -> None:
                print("dummy")


def create_plugin(path: Path) -> None:
    path.mkdir(parents=True)
    init = path / "__init__.py"
    init.write_text(
        "from tests.integration.test_plugins_flow import DummyPlugin as Plugin\n"
    )


def test_plugins_flow(tmp_path: Path):
    plugin_src = tmp_path / "src"
    create_plugin(plugin_src)
    plugin_dir = tmp_path / "plugins"
    mgr = PluginManager(plugin_dir=plugin_dir)

    # 1. install and activate
    mgr.install(plugin_src)
    mgr.discover()
    mgr.activate("dummy")
    assert "dummy" in mgr._active

    # 2. register commands
    import click

    @click.group()
    def cli():
        pass

    mgr.cli = cli
    mgr.activate("dummy")
    assert "dummy-cmd" in cli.commands

    # 3. deactivate and uninstall
    mgr.deactivate("dummy")
    assert "dummy" not in mgr._active
    mgr.uninstall("src")
    assert not (plugin_dir / "src").exists()
