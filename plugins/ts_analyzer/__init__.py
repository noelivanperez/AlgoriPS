from algorips.core.plugins.contract import BasePlugin

class Plugin(BasePlugin):
    def name(self) -> str:
        return "ts-analyzer"

    def version(self) -> str:
        return "0.1"

    def register(self, cli, gui_registry) -> None:
        if cli:
            @cli.command("ts-check")
            def ts_check() -> None:
                print("TypeScript analysis")
