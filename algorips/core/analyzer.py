from __future__ import annotations

import pathlib
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    path: str
    line_count: int


def analyze_path(path: str) -> AnalysisResult:
    """Analyze a Python project by counting lines of code."""
    project_path = pathlib.Path(path)
    total_lines = 0
    for py_file in project_path.rglob('*.py'):
        total_lines += py_file.read_text().count('\n')
    return AnalysisResult(path=str(project_path), line_count=total_lines)
