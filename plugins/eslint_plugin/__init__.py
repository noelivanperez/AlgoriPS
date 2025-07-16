from algorips.core.plugins.contract import BasePlugin

class Plugin(BasePlugin):
    def name(self) -> str:
        return "eslint-plugin"

    def version(self) -> str:
        return "0.1"

    def register(self, cli, gui_registry) -> None:
        if cli:
            @cli.command("eslint-run")
            def eslint_run() -> None:
                print("Run ESLint")
