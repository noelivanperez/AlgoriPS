"""Quality rules for semantic analysis."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class Rule:
    id: str
    description: str
    threshold: int


class RuleSet:
    """Container for quality rules."""

    def __init__(self) -> None:
        self.rules: Dict[str, Rule] = {
            "F001": Rule(
                id="F001",
                description="Function too long",
                threshold=50,
            ),
            "C001": Rule(
                id="C001",
                description="Too many methods in class",
                threshold=10,
            ),
            "C002": Rule(
                id="C002",
                description="Class complexity high",
                threshold=5,
            ),
        }

    def get(self, rule_id: str) -> Rule | None:
        return self.rules.get(rule_id)
