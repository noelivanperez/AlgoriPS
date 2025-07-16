"""Simple retrieval augmented generation utilities."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Callable, Iterable, List, Tuple


Vector = List[float]


def _cosine_similarity(a: Vector, b: Vector) -> float:
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na and nb:
        return dot / (na * nb)
    return 0.0


class JSONVectorStore:
    """Very small JSON based vector store."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.data: List[dict] = []
        self.load()

    def add(self, text: str, vector: Vector) -> None:
        self.data.append({"text": text, "vector": vector})

    def search(self, vector: Vector, top_k: int = 3) -> List[Tuple[str, float]]:
        results = [
            (item["text"], _cosine_similarity(vector, item["vector"]))
            for item in self.data
        ]
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def save(self) -> None:
        with self.path.open("w") as f:
            json.dump(self.data, f)

    def load(self) -> None:
        if self.path.exists():
            self.data = json.loads(self.path.read_text())
        else:
            self.data = []


try:  # optional faiss support
    import faiss  # type: ignore
    import numpy as np  # type: ignore

    class FAISSVectorStore(JSONVectorStore):
        def __init__(self, path: str | Path, dim: int) -> None:
            self.index_path = Path(path).with_suffix(".index")
            super().__init__(Path(path).with_suffix(".json"))
            self.dim = dim
            if self.index_path.exists():
                self.index = faiss.read_index(str(self.index_path))
            else:
                self.index = faiss.IndexFlatL2(dim)

        def add(self, text: str, vector: Vector) -> None:
            import numpy as np

            v = np.array(vector, dtype="float32").reshape(1, -1)
            self.index.add(v)
            self.data.append({"text": text, "vector": vector})

        def search(self, vector: Vector, top_k: int = 3) -> List[Tuple[str, float]]:
            import numpy as np

            v = np.array(vector, dtype="float32").reshape(1, -1)
            D, I = self.index.search(v, top_k)
            results = []
            for idx, dist in zip(I[0], D[0]):
                if idx == -1:
                    continue
                text = self.data[int(idx)]["text"]
                results.append((text, float(-dist)))
            results.sort(key=lambda x: x[1], reverse=True)
            return results

        def save(self) -> None:
            super().save()
            faiss.write_index(self.index, str(self.index_path))

except Exception:  # pragma: no cover - faiss not available
    FAISSVectorStore = None  # type: ignore


class RAGEngine:
    """Load documents, embed them and perform simple retrieval."""

    def __init__(
        self,
        docs: Iterable[str | Path],
        store_path: str | Path | None = None,
        embed_fn: Callable[[str], Vector] | None = None,
        use_faiss: bool = True,
    ) -> None:
        self.docs = [Path(d) for d in docs]
        self.embed_fn = embed_fn or self._default_embed
        store = store_path or "rag_store.json"
        self.use_faiss = use_faiss and FAISSVectorStore is not None
        self.store_path = Path(store)
        self.store: JSONVectorStore | FAISSVectorStore
        if self.use_faiss:
            # dim will be determined on first embed
            self.store = FAISSVectorStore(self.store_path, 0)  # type: ignore[arg-type]
        else:
            self.store = JSONVectorStore(self.store_path)

    def _default_embed(self, text: str) -> Vector:
        return [float(ord(c)) for c in text][:32]

    @staticmethod
    def _read_text(path: Path) -> str:
        if path.suffix.lower() == ".pdf":
            try:
                from pdfminer.high_level import extract_text  # type: ignore

                return extract_text(str(path))
            except Exception:
                return ""
        return path.read_text(encoding="utf-8")

    def ingest(self) -> None:
        texts: List[str] = []
        for doc in self.docs:
            if not doc.exists():
                continue
            text = self._read_text(doc)
            for line in text.splitlines():
                line = line.strip()
                if line:
                    texts.append(line)
        if not texts:
            return
        embeddings = [self.embed_fn(t) for t in texts]
        if self.use_faiss:
            # recreate index with correct dimension if needed
            dim = len(embeddings[0])
            self.store = FAISSVectorStore(self.store_path, dim)  # type: ignore[arg-type]
        for text, vec in zip(texts, embeddings):
            self.store.add(text, vec)
        self.store.save()

    def query(self, text: str, top_k: int = 3) -> List[str]:
        if not getattr(self.store, "data", None):
            # try load
            self.store.load()
        vec = self.embed_fn(text)
        results = self.store.search(vec, top_k)
        return [t for t, _ in results]
