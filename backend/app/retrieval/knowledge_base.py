from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from app.retrieval.hybrid_search import HybridSearch
from app.retrieval.reranker import CrossEncoderReranker
from app.retrieval.vector_store import VectorStore


DEFAULT_CHUNKS_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "knowledge_chunks.jsonl"
)


def load_documents(chunks_path: Path = DEFAULT_CHUNKS_PATH) -> list[dict]:
    documents = []
    with chunks_path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                documents.append(json.loads(line))
    return documents


@lru_cache(maxsize=1)
def get_knowledge_searcher() -> HybridSearch:
    documents = load_documents()
    vector_store = VectorStore()

    for document in documents:
        vector_store.add(document["text"], document)

    reranker = CrossEncoderReranker()
    return HybridSearch(documents, vector_store, reranker)
