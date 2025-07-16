import importlib
from pathlib import Path
import click

from algorips.core.server import app

PLUGIN_DIR = Path(__file__).resolve().parents[1] / "plugins"

def load_plugins() -> None:
    if not PLUGIN_DIR.exists():
        return
    for path in PLUGIN_DIR.rglob("*.py"):
        rel = path.relative_to(PLUGIN_DIR).with_suffix("")
        module = ".".join(["plugins"] + list(rel.parts))
        importlib.import_module(module)

@click.group()
def cli() -> None:
    """AlgoriPS main CLI."""

@cli.command()
def serve() -> None:
    """Start the HTTP server."""
    load_plugins()
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    cli()
