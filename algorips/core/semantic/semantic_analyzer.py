"""Semantic analyzer for Python code."""
from __future__ import annotations

import ast
import json
import pathlib
from dataclasses import dataclass
from typing import Any, Dict, Iterable

import networkx as nx


@dataclass
class NodeInfo:
    name: str
    type: str
    location: str


class SemanticAnalyzer:
    """Analyze Python source code and build a dependency graph."""

    def build_graph(self, path: str) -> nx.DiGraph:
        root = pathlib.Path(path)
        graph: nx.DiGraph = nx.DiGraph()

        for py_file in root.rglob("*.py"):
            if any(part in {"__pycache__", ".git"} for part in py_file.parts):
                continue
            module_id = str(py_file)
            graph.add_node(module_id, type="module", location=str(py_file))

            tree = ast.parse(py_file.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_id = f"{py_file}:{node.name}"
                    graph.add_node(
                        func_id,
                        type="function",
                        location=f"{py_file}:{node.lineno}",
                    )
                    graph.add_edge(module_id, func_id, type="contains")
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call):
                            if isinstance(child.func, ast.Name):
                                target = f"{py_file}:{child.func.id}"
                                graph.add_edge(func_id, target, type="call")
                        if isinstance(child, ast.Attribute):
                            if isinstance(child.value, ast.Name):
                                target = f"{py_file}:{child.attr}"
                                graph.add_edge(func_id, target, type="call")
                elif isinstance(node, ast.ClassDef):
                    class_id = f"{py_file}:{node.name}"
                    graph.add_node(
                        class_id,
                        type="class",
                        location=f"{py_file}:{node.lineno}",
                    )
                    graph.add_edge(module_id, class_id, type="contains")
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            target = f"{py_file}:{base.id}"
                            graph.add_edge(class_id, target, type="inheritance")
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    for alias in node.names:
                        target = alias.name
                        graph.add_edge(module_id, target, type="import")

        return graph

    def to_json(self, graph: nx.DiGraph) -> str:
        data: Dict[str, Any] = {
            "nodes": [
                {
                    "id": n,
                    "type": graph.nodes[n].get("type"),
                    "location": graph.nodes[n].get("location"),
                }
                for n in graph.nodes
            ],
            "edges": [
                {
                    "source": u,
                    "target": v,
                    "type": graph.edges[u, v].get("type"),
                }
                for u, v in graph.edges
            ],
        }
        return json.dumps(data, indent=2)
