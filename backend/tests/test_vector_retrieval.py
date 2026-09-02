from __future__ import annotations

import sys
import unittest
from collections.abc import Sequence
from pathlib import Path
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.retrieval import vector_store


class _FakeSentenceModel:
    def get_embedding_dimension(self) -> int:
        return len(_FakeEmbeddingModel.VOCABULARY)


class _FakeEmbeddingModel:
    VOCABULARY = (
        "payment",
        "service",
        "database",
        "connection",
        "pool",
        "exhausted",
        "timeout",
        "authentication",
        "jwt",
        "redis",
        "cache",
        "recommendation",
    )

    def __init__(self) -> None:
        self.model = _FakeSentenceModel()

    def encode(self, text: str | Sequence[str]) -> np.ndarray:
        if isinstance(text, str):
            return self._encode_one(text)

        return np.asarray([self._encode_one(item) for item in text], dtype=np.float32)

    def _encode_one(self, text: str) -> np.ndarray:
        normalized = text.lower()
        return np.asarray(
            [float(term in normalized) for term in self.VOCABULARY],
            dtype=np.float32,
        )


class VectorRetrievalTest(unittest.TestCase):
    def test_vector_search_returns_payment_documents_first(self) -> None:
        with patch.object(vector_store, "EmbeddingModel", _FakeEmbeddingModel):
            store = vector_store.VectorStore()

        documents = [
            "Payment database connection pool exhausted. "
            "Increase database connection pool size and restart payment service.",
            "Payment service experiencing database connection timeout errors.",
            "Authentication service JWT tokens are expired.",
            "Redis cache unavailable for recommendation service.",
        ]

        for chunk_index, document in enumerate(documents):
            store.add(
                document,
                {
                    "chunk_id": f"chunk-{chunk_index}",
                    "document_id": f"document-{chunk_index}",
                    "source_path": f"test/document_{chunk_index}.md",
                    "category": "runbooks" if chunk_index < 2 else "incidents",
                    "title": f"Test Document {chunk_index}",
                    "chunk_index": chunk_index,
                    "section": "Test",
                },
            )

        results = store.search("payment service database connection pool exhausted", k=4)

        for result in results:
            metadata = result["metadata"]
            print(f"{result['score']:.2f} | {metadata.title} | {metadata.text}")

        top_texts = [result["metadata"].text for result in results[:2]]
        self.assertIn("Payment database connection pool exhausted.", top_texts[0])
        self.assertIn(
            "Payment service experiencing database connection timeout errors.",
            top_texts[1],
        )
