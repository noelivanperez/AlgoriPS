from __future__ import annotations

import pathlib
import re
from dataclasses import dataclass
from typing import Dict


@dataclass
class AnalysisResult:
    """Metrics collected from scanning Python files."""

    path: str
    line_count: int
    function_count: int
    class_count: int


class CodeAnalyzer:
    """Analyze Python source code for basic metrics."""

    def scan(self, path: str) -> Dict[str, int | str]:
        """Return metrics for Python files under *path*.

        The analyzer walks the directory recursively, ignoring ``__pycache__`` and
        ``.git`` folders. Each Python file contributes to the total line count and
        counts of ``def`` and ``class`` statements.
        """

        project_path = pathlib.Path(path)
        metrics = {
            "path": str(project_path),
            "line_count": 0,
            "function_count": 0,
            "class_count": 0,
        }

        pattern_func = re.compile(r"^\s*def\s+", re.MULTILINE)
        pattern_class = re.compile(r"^\s*class\s+", re.MULTILINE)

        for py_file in project_path.rglob("*.py"):
            if any(part in {"__pycache__", ".git"} for part in py_file.parts):
                continue

            text = py_file.read_text(encoding="utf-8")
            metrics["line_count"] += len(text.splitlines())
            metrics["function_count"] += len(pattern_func.findall(text))
            metrics["class_count"] += len(pattern_class.findall(text))

        return metrics