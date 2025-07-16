from algorips.core.plugins.contract import BasePlugin

class Plugin(BasePlugin):
    def name(self) -> str:
        return "eslint-plugin"

    def version(self) -> str:
        return "0.1"

    @property
    def description(self) -> str:
        return "Run ESLint on JavaScript/TypeScript code"

    @property
    def dependencies(self) -> list[str]:
        return []

    def register(self, cli, gui_registry) -> None:
        if cli:
            @cli.command("eslint-run")
            def eslint_run() -> None:
                print("Run ESLint")
