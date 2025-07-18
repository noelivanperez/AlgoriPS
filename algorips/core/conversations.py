from __future__ import annotations

from typing import List, Dict, Optional
from sqlalchemy import text

from .db import get_session


def save(prompt: str, response: str) -> None:
    """Persist prompt and response in the conversations table."""
    with get_session() as session:
        session.execute(
            text("INSERT INTO conversations (prompt, response) VALUES (:p, :r)"),
            {"p": prompt, "r": response},
        )
        session.commit()


def delete(conv_id: Optional[int] = None) -> None:
    """Delete a conversation by ID or all if ID is None."""
    with get_session() as session:
        if conv_id is None:
            session.execute(text("DELETE FROM conversations"))
        else:
            session.execute(
                text("DELETE FROM conversations WHERE id=:id"),
                {"id": conv_id},
            )
        session.commit()


def list_all() -> List[Dict[str, object]]:
    """Return all conversations ordered by ID."""
    with get_session() as session:
        result = session.execute(
            text("SELECT id, prompt, response, timestamp FROM conversations ORDER BY id")
        ).mappings()
        return [dict(row) for row in result]
