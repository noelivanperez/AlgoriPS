import json
from pathlib import Path

import click

from algorips import __version__
from algorips.core.analyzer import CodeAnalyzer

DEFAULT_CONFIG = (
    "database:\n"
    "  url: mysql+pymysql://root:example@localhost/algorips\n"
    "ollama_url: http://localhost:11434\n"
)


@click.group()
@click.version_option(__version__)
def cli() -> None:
    """AlgoriPS command line interface."""


@cli.command()
def init() -> None:
    """Create default configuration file."""
    cfg = Path("algorips.yaml")
    if cfg.exists():
        click.echo(f"{cfg} already exists.")
        return
    cfg.write_text(DEFAULT_CONFIG)
    click.echo(f"Created {cfg}")


@cli.command()
@click.argument('path', default='.')
def analyze(path: str) -> None:
    """Run code analysis on the given PATH."""
    analyzer = CodeAnalyzer()
    result = analyzer.scan(path)
    click.echo(json.dumps(result, indent=2))


if __name__ == '__main__':
    cli()
