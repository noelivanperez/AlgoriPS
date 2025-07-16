from algorips.core.analyzer import CodeAnalyzer


def test_code_analyzer_counts(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text("""\
def foo():
    pass

class Bar:
    pass
""")

    analyzer = CodeAnalyzer()
    result = analyzer.scan(str(tmp_path))

    assert result["line_count"] == 5
    assert result["function_count"] == 1
    assert result["class_count"] == 1
