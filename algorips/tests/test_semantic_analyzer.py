from algorips.core.semantic.semantic_analyzer import SemanticAnalyzer


def test_semantic_analyzer_builds_graph(tmp_path):
    (tmp_path / "sample.py").write_text(
        """\
import math

def foo():
    return math.sqrt(4)
"""
    )
    analyzer = SemanticAnalyzer()
    graph = analyzer.build_graph(str(tmp_path))
    # expect nodes for module and function
    assert any("sample.py" in n for n in graph.nodes)
    assert any(data.get("type") == "function" for _, data in graph.nodes(data=True))
    # there should be an import edge
    assert any(d.get("type") == "import" for _, _, d in graph.edges(data=True))


def test_semantic_to_json(tmp_path):
    (tmp_path / "a.py").write_text("def foo():\n    pass\n")
    analyzer = SemanticAnalyzer()
    graph = analyzer.build_graph(str(tmp_path))
    json_str = analyzer.to_json(graph)
    assert "nodes" in json_str
    assert "edges" in json_str

