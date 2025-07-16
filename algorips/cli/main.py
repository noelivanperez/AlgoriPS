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

@click.option("--deep", is_flag=True, help="Perform deep semantic analysis")
@click.argument("path", default=".")
def analyze(path: str, deep: bool) -> None:
    """Run code analysis on the given PATH."""
    if deep:
        from algorips.core.semantic.semantic_analyzer import SemanticAnalyzer
        analyzer = SemanticAnalyzer()
        graph = analyzer.build_graph(path)
        click.echo(analyzer.to_json(graph))
    else:
        analyzer = CodeAnalyzer()
        result = analyzer.scan(path)
        click.echo(json.dumps(result, indent=2))

@cli.command()
@click.argument("rule_id")
@click.argument("file_path")
def apply_rule(rule_id: str, file_path: str) -> None:
    """Apply refactor patch for RULE_ID to FILE_PATH."""
    from algorips.core.semantic.patcher import Patcher

    patcher = Patcher()
    patch = patcher.generate_patch(rule_id, file_path)
    if not patch:
        click.echo("No patch generated")
        return
    if patcher.apply_patch(patch):
        click.echo("Patch applied")
    else:
        click.echo("Failed to apply patch")

if __name__ == '__main__':
    cli()
