"""Utilities to generate and apply patches."""
from __future__ import annotations

import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


class Patcher:
    """Generate and apply diffs based on rules."""

    def generate_patch(self, rule_id: str, file_path: str) -> str:
        """Return a unified diff string for the given rule."""
        path = Path(file_path)
        rel = path.name
        if rule_id == "F001":
            text = path.read_text()
            patched = text.rstrip() + "\n"
            with TemporaryDirectory() as td:
                orig = Path(td) / "orig"
                mod = Path(td) / "mod"
                orig.write_text(text)
                mod.write_text(patched)
                res = subprocess.run(
                    ["git", "diff", "--no-index", "--patch", orig, mod],
                    capture_output=True,
                    text=True,
                )
                patch = res.stdout.replace(str(orig), f"a/{rel}").replace(str(mod), f"b/{rel}")
                return patch
        return ""

    def apply_patch(self, patch: str, cwd: str | None = None) -> bool:
        """Apply a patch using git apply."""
        check = subprocess.run(
            ["git", "apply", "--check"], cwd=cwd, input=patch.encode(), capture_output=True
        )
        if check.returncode != 0:
            return False
        apply = subprocess.run(["git", "apply"], cwd=cwd, input=patch.encode())
        return apply.returncode == 0
