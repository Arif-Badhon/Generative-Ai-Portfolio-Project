import pytest
from app.core.embeddings import EmbeddingGenerator

def test_embedding_generation():
    embedder = EmbeddingGenerator("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = embedder.generate(["test text"])
    assert len(embeddings) == 1
    assert len(embeddings[0]) == 384

# Run tests with: uv run pytest
