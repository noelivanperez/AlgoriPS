import json
import click

from algorips.core.analyzer import analyze_path
from algorips.core.db import get_engine


@click.group()
def cli() -> None:
    """AlgoriPS command line interface."""


@cli.command()
def init() -> None:
    """Initialize connections to required services."""
    engine = get_engine()
    # attempt connection
    with engine.connect() as conn:
        conn.execute("SELECT 1")
    click.echo("Initialization successful.")


@cli.command()
@click.argument('path', default='.')
def analyze(path: str) -> None:
    """Run code analysis on the given PATH."""
    result = analyze_path(path)
    click.echo(json.dumps(result.__dict__, indent=2))


if __name__ == '__main__':
    cli()
