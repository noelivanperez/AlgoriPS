from __future__ import annotations

import pathlib
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    path: str
    line_count: int


class CodeAnalyzer:
    """Simple analyzer that counts Python lines."""

    def scan(self, path: str) -> AnalysisResult:
        project_path = pathlib.Path(path)
        total_lines = 0
        for py_file in project_path.rglob('*.py'):
            total_lines += py_file.read_text().count('\n')
        return AnalysisResult(path=str(project_path), line_count=total_lines)
