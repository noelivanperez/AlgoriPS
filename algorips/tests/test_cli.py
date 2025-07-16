from click.testing import CliRunner
from pathlib import Path

from algorips.cli.main import cli


def test_init_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'init' in result.output
    assert 'analyze' in result.output


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
