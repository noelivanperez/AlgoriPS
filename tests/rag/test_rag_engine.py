from pathlib import Path

from algorips.core.rag import RAGEngine


def test_ingest_creates_store(tmp_path: Path):
    doc = tmp_path / "d1.txt"
    doc.write_text("hello world")

    engine = RAGEngine([doc], store_path=tmp_path / "store.json", embed_fn=lambda t: [1.0])
    engine.ingest()

    store_file = tmp_path / "store.json"
    assert store_file.exists()
    data = store_file.read_text()
    assert "hello world" in data


def test_query_returns_expected(tmp_path: Path):
    d1 = tmp_path / "a.txt"
    d2 = tmp_path / "b.txt"
    d1.write_text("alpha")
    d2.write_text("beta")

    def fake_embed(text: str):
        mapping = {
            "alpha": [1.0, 0.0],
            "beta": [0.0, 1.0],
            "query": [1.0, 0.0],
        }
        return mapping.get(text.strip(), [0.0, 0.0])

    engine = RAGEngine([d1, d2], store_path=tmp_path / "store.json", embed_fn=fake_embed)
    engine.ingest()

    results = engine.query("query")
    assert results and results[0] == "alpha"
