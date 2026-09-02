from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import faiss
from app.retrieval.embeddings import EmbeddingModel

@dataclass(frozen=True)
class VectorMetadata:
    chunk_id: str
    document_id: str
    source_path: str
    category: str
    title: str | None
    chunk_index: int
    text: str
    section: str | None

class VectorStore:

    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.dimension = self.embedding_model.model.get_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata: dict[int, VectorMetadata] = {}
    
    def add(self, text: str, metadata: dict) -> None:
        vector_array = self.embedding_model.encode(text).reshape(1, -1)
        index_id = self.index.ntotal
        self.index.add(vector_array)
        self.metadata[index_id] = VectorMetadata(
            chunk_id=metadata["chunk_id"],
            document_id=metadata["document_id"],
            source_path=metadata["source_path"],
            category=metadata["category"],
            title=metadata.get("title"),
            chunk_index=metadata["chunk_index"],
            text=text,
            section=metadata.get("section"),
        )
    
    def search(self, query: str, k: int = 5) -> list[dict[str, Any]]:
        k = min(k, self.index.ntotal)

        if k == 0:
            return []
        search_results = []
        query_array = self.embedding_model.encode(query).reshape(1, -1)

        distances, indices = self.index.search(query_array, k)

        for distance, index_id in zip(distances[0], indices[0]):
            index_id = int(index_id)

            if index_id == -1:
                continue

            metadata = self.metadata.get(index_id)
            if metadata is None:
                continue

            search_results.append(
                {
                    "score": float(distance),
                    "metadata": metadata,
                }
            )

        return search_results
