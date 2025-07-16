"""Utilities for interacting with a local git repository."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


def _run(cmd: list[str], cwd: Optional[str] = None) -> None:
    """Run *cmd* raising ``CalledProcessError`` on failure."""
    subprocess.run(cmd, cwd=cwd, check=True)


def clone(repo_url: str, dest_path: str) -> Path:
    """Clone *repo_url* into *dest_path* and return the path."""
    _run(["git", "clone", repo_url, dest_path])
    return Path(dest_path)


def checkout_branch(branch_name: str, create: bool = False, cwd: str = ".") -> None:
    """Checkout the given branch in the repository located at *cwd*."""
    args = ["git", "checkout"]
    if create:
        args += ["-b", branch_name]
    else:
        args.append(branch_name)
    _run(args, cwd=cwd)


def commit_all(message: str, cwd: str = ".") -> None:
    """Stage all changes and create a commit with *message*."""
    _run(["git", "add", "-A"], cwd=cwd)
    _run(["git", "commit", "-m", message], cwd=cwd)


def push(branch_name: str, cwd: str = ".") -> None:
    """Push *branch_name* to origin."""
    _run(["git", "push", "-u", "origin", branch_name], cwd=cwd)
