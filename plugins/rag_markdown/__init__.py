from __future__ import annotations

import click

from algorips.core.plugins.contract import BasePlugin
from algorips.core.rag import RAGEngine


class Plugin(BasePlugin):
    def name(self) -> str:
        return "rag-markdown"

    def version(self) -> str:
        return "0.1"

    def register(self, cli, gui_registry) -> None:
        if cli:
            @cli.command("rag-md")
            @click.argument("docs", nargs=-1, type=click.Path(exists=True))
            @click.option("--query", "query_text", required=True)
            def rag_md(docs: tuple[str, ...], query_text: str) -> None:
                engine = RAGEngine(docs, use_faiss=False)
                engine.ingest()
                results = engine.query(query_text)
                for res in results:
                    click.echo(res)
