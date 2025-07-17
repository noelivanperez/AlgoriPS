import json
import itertools
import threading
import time
from pathlib import Path
import subprocess

import click

from algorips import __version__
from algorips.core.analyzer import CodeAnalyzer
from algorips.core import scraper, config as cfg
from algorips.core.llm import OllamaProvider
from algorips.core.git import local
from algorips.core.git.github import GitHubClient
from algorips.core.plugins import PluginManager
from algorips.core.rag import RAGEngine
from algorips.core.ollama_client import OllamaClient

DEFAULT_CONFIG = (
    "database:\n"
    "  url: mysql+pymysql://root:example@localhost/algorips\n"
    "ollama_url: http://localhost:11434\n"
    "ollama_model: llama3\n"
)

CONFIG = cfg.load()
provider = OllamaProvider()


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


@cli.command()
@click.argument("prompt", nargs=-1)
@click.option("--model", default=None, help="Ollama model to use")
def chat(prompt: tuple[str, ...], model: str | None) -> None:
    """Send PROMPT to Ollama and print the response."""
    mdl = model or CONFIG.get("model")
    if not provider.model_exists(mdl):
        click.echo(f"Model '{mdl}' not available", err=True)
        raise click.Abort()
    text = " ".join(prompt)

    stop = threading.Event()

    def spinner() -> None:
        for ch in itertools.cycle("|/-\\"):
            if stop.is_set():
                break
            click.echo(ch, nl=False)
            click.echo("\b", nl=False)
            time.sleep(0.1)

    t = threading.Thread(target=spinner)
    t.start()
    try:
        result = provider.send_prompt(text, mdl)
    finally:
        stop.set()
        t.join()
    click.echo(json.dumps(result, indent=2))
    CONFIG["model"] = mdl
    cfg.save(CONFIG)


@cli.command("rag")
@click.argument("docs", nargs=-1, type=click.Path(exists=True))
@click.option("--query", "query_text", required=True)
def rag_cmd(docs: tuple[str, ...], query_text: str) -> None:
    """Query documents using a simple RAG engine."""
    engine = RAGEngine(docs, use_faiss=False)
    engine.ingest()
    results = engine.query(query_text)
    for res in results:
        click.echo(res)


@cli.command()
@click.argument("config_path")
def scrape(config_path: str) -> None:
    """Scrape pages defined in CONFIG_PATH."""
    cfg = scraper.load_config(config_path)
    results = scraper.WebScraper(cfg).scrape()
    click.echo(json.dumps(results, indent=2))


@cli.group()
def repo() -> None:
    """Repository management commands."""


@repo.command()
@click.argument("url")
@click.option("--dest", default=".", help="Destination directory")
def clone(url: str, dest: str) -> None:
    """Clone a repository."""
    local.clone(url, dest)
    click.echo(f"Cloned into {dest}")


@repo.command()
@click.argument("name")
def branch(name: str) -> None:
    """Create and checkout a new branch."""
    local.checkout_branch(name, create=True)
    click.echo(f"Switched to {name}")


@repo.command()
@click.argument("message")
def commit(message: str) -> None:
    """Commit all changes with MESSAGE."""
    local.commit_all(message)
    click.echo("Commit created")


@repo.group()
def pr() -> None:
    """Pull request operations."""


@pr.command("create")
@click.option("--owner", required=True)
@click.option("--repo", "repo_name", required=True)
@click.option("--base", default="main")
@click.option("--reviewers", default="")
@click.option("--labels", default="")
@click.option("--token", envvar="GITHUB_TOKEN", required=True)
@click.argument("title")
@click.option("--body", default="")
def pr_create(owner: str, repo_name: str, base: str, reviewers: str, labels: str, token: str, title: str, body: str) -> None:
    """Create a pull request from current branch."""
    head = subprocess.run([
        "git",
        "rev-parse",
        "--abbrev-ref",
        "HEAD",
    ], capture_output=True, text=True, check=True).stdout.strip()
    client = GitHubClient(token)
    pr = client.create_pull_request(
        owner,
        repo_name,
        head,
        base,
        title,
        body,
        reviewers.split(",") if reviewers else None,
        labels.split(",") if labels else None,
    )
    click.echo(f"Created PR #{pr['number']}")


@pr.command("merge")
@click.argument("pr_number", type=int)
@click.option("--owner", required=True)
@click.option("--repo", "repo_name", required=True)
@click.option("--token", envvar="GITHUB_TOKEN", required=True)
def pr_merge(pr_number: int, owner: str, repo_name: str, token: str) -> None:
    """Merge the given pull request."""
    client = GitHubClient(token)
    result = client.merge_pull_request(owner, repo_name, pr_number)
    if result.get("merged"):
        click.echo("PR merged")
    else:
        click.echo("Merge failed")


# Plugin commands
plugin_manager = PluginManager()


@cli.group()
def models() -> None:
    """Model related commands."""


@models.command("ls")
def models_ls() -> None:
    """List available Ollama models."""
    try:
        for name in provider.list_models():
            click.echo(name)
    except Exception as exc:
        click.echo(f"Failed to list models: {exc}", err=True)


@cli.group()
def ollama() -> None:
    """Ollama helper commands."""


@ollama.command("status")
def ollama_status() -> None:
    """Check if the Ollama server is reachable."""
    if provider.health():
        click.echo("Ollama is up")
    else:
        click.echo("Ollama is unreachable", err=True)


@cli.group()
def plugin() -> None:
    """Plugin management commands."""


@plugin.command("list")
def plugin_list() -> None:
    """List installed plugins."""
    for info in plugin_manager.list_plugins():
        status = "[active]" if info["active"] else ""
        click.echo(f"{info['name']} {info['version']} {status}")


@plugin.command("install")
@click.argument("path")
def plugin_install(path: str) -> None:
    """Install plugin from PATH or URL."""
    plugin_manager.install(path)
    click.echo("Plugin installed")


@plugin.command("uninstall")
@click.argument("name")
def plugin_uninstall(name: str) -> None:
    """Uninstall plugin by NAME."""
    plugin_manager.uninstall(name)
    click.echo("Plugin uninstalled")


@cli.group()
def ollama() -> None:
    """Interact with the Ollama language model."""


@ollama.command("chat")
@click.argument("prompt")
@click.option("--model", default=None, help="Model to use")
def ollama_chat(prompt: str, model: str | None) -> None:
    """Send PROMPT to Ollama and print the response."""
    client = OllamaClient(model=model)
    result = client.send_prompt(prompt)
    click.echo(json.dumps(result, indent=2))

if __name__ == '__main__':
    cli()
