from click.testing import CliRunner
from pathlib import Path
import subprocess

from algorips.cli.main import cli


def test_init_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'init' in result.output
    assert 'analyze' in result.output
    assert 'repo' in result.output


def test_init_creates_config():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['init'])
        assert result.exit_code == 0
        assert Path('algorips.yaml').exists()


def test_analyze_smoke(tmp_path):
    test_file = tmp_path / 'sample.py'
    test_file.write_text('print("hello")\n')
    runner = CliRunner()
    result = runner.invoke(cli, ['analyze', str(tmp_path)])
    assert result.exit_code == 0
    assert 'line_count' in result.output
    assert 'function_count' in result.output
    assert 'class_count' in result.output


def test_repo_branch(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem():
        subprocess.run(['git', 'init', '-b', 'main'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'a@b.c'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'], check=True)
        Path('dummy.txt').write_text('x')
        subprocess.run(['git', 'add', 'dummy.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', 'init'], check=True)
        result = runner.invoke(cli, ['repo', 'branch', 'feature'])
        assert result.exit_code == 0
        head = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
        assert head == 'feature'
