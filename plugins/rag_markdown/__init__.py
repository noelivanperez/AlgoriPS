from algorips.core.plugins.contract import BasePlugin

class Plugin(BasePlugin):
    def name(self) -> str:
        return "rag-markdown"

    def version(self) -> str:
        return "0.1"

    def register(self, cli, gui_registry) -> None:
        if cli:
            @cli.command("rag-md")
            def rag_md() -> None:
                print("RAG Markdown")
