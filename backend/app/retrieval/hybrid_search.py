from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from app.retrieval.bm25 import BM25Retriever, BM25SearchResult
from app.retrieval.vector_store import VectorMetadata, VectorStore


@dataclass(frozen=True)
class HybridSearchResult:
    text: str
    metadata: VectorMetadata | dict[str, Any] | None
    bm25_score: float = 0.0
    vector_score: float = 0.0
    combined_score: float = 0.0
    reranker_score: float | None = None


class HybridSearch:
    def __init__(
        self,
        documents: Sequence[str | VectorMetadata | dict[str, Any]],
        vector_store: VectorStore,
        reranker: Any | None = None,
    ) -> None:
        self.documents = list(documents)
        self.bm25 = BM25Retriever(self.documents)
        self.vector_store = vector_store
        self.reranker = reranker

    def retrieve_bm25(
        self,
        query: str,
        candidate_k: int = 20,
    ) -> list[BM25SearchResult]:
        return self.bm25.search(query, k=candidate_k)

    def retrieve_vector(
        self,
        query: str,
        candidate_k: int = 20,
    ) -> list[dict[str, Any]]:
        return self.vector_store.search(query, k=candidate_k)

    def normalize_scores(self, scores: Sequence[float]) -> list[float]:
        if not scores:
            return []

        minimum = min(scores)
        maximum = max(scores)

        if minimum == maximum:
            if maximum == 0:
                return [0.0 for _ in scores]
            return [1.0 for _ in scores]

        return [(score - minimum) / (maximum - minimum) for score in scores]

    def combine_results(
        self,
        bm25_results: Sequence[BM25SearchResult],
        vector_results: Sequence[dict[str, Any]],
        bm25_weight: float = 0.5,
        vector_weight: float = 0.5,
    ) -> list[HybridSearchResult]:
        result_data = {}

        for result in bm25_results:
            if isinstance(result.metadata, VectorMetadata):
                result_id = result.metadata.chunk_id
            elif isinstance(result.metadata, dict):
                result_id = result.metadata.get("chunk_id", result.text)
            else:
                result_id = result.text

            result_data[result_id] = {
                "text": result.text,
                "metadata": result.metadata,
                "bm25_score": result.score,
                "vector_score": 0.0,
            }

        for result in vector_results:
            metadata = result.get("metadata")
            if isinstance(metadata, VectorMetadata):
                result_id = metadata.chunk_id
                text = metadata.text
            elif isinstance(metadata, dict):
                result_id = metadata.get("chunk_id", metadata.get("text", ""))
                text = metadata.get("text", "")
            else:
                result_id = str(metadata)
                text = ""

            distance = float(result.get("score", 0.0))
            vector_score = 1 / (1 + distance)

            if result_id not in result_data:
                result_data[result_id] = {
                    "text": text,
                    "metadata": metadata,
                    "bm25_score": 0.0,
                    "vector_score": vector_score,
                }
            else:
                result_data[result_id]["vector_score"] = vector_score

        bm25_scores = [item["bm25_score"] for item in result_data.values()]
        vector_scores = [item["vector_score"] for item in result_data.values()]
        normalized_bm25 = self.normalize_scores(bm25_scores)
        normalized_vector = self.normalize_scores(vector_scores)

        combined_results = []
        for index, item in enumerate(result_data.values()):
            combined_score = (
                bm25_weight * normalized_bm25[index]
                + vector_weight * normalized_vector[index]
            )
            combined_results.append(
                HybridSearchResult(
                    text=item["text"],
                    metadata=item["metadata"],
                    bm25_score=item["bm25_score"],
                    vector_score=item["vector_score"],
                    combined_score=combined_score,
                )
            )

        combined_results.sort(
            key=lambda result: result.combined_score,
            reverse=True,
        )
        return combined_results

    def rerank(
        self,
        query: str,
        candidates: Sequence[HybridSearchResult],
    ) -> list[HybridSearchResult]:
        if self.reranker is None:
            return list(candidates)

        pairs = [[query, result.text] for result in candidates]
        scores = self.reranker.predict(pairs)
        reranked_results = []

        for result, score in zip(candidates, scores):
            reranked_results.append(
                HybridSearchResult(
                    text=result.text,
                    metadata=result.metadata,
                    bm25_score=result.bm25_score,
                    vector_score=result.vector_score,
                    combined_score=result.combined_score,
                    reranker_score=float(score),
                )
            )

        reranked_results.sort(
            key=lambda result: (
                result.reranker_score
                if result.reranker_score is not None
                else 0.0
            ),
            reverse=True,
        )
        return reranked_results

    def search(
        self,
        query: str,
        k: int = 5,
        candidate_k: int = 20,
        use_reranker: bool = True,
    ) -> list[HybridSearchResult]:
        bm25_results = self.retrieve_bm25(query, candidate_k=candidate_k)
        vector_results = self.retrieve_vector(query, candidate_k=candidate_k)
        combined_results = self.combine_results(bm25_results, vector_results)

        if use_reranker and self.reranker is not None:
            combined_results = self.rerank(query, combined_results)
            combined_results.sort(
                key=lambda result: (
                    result.reranker_score
                    if result.reranker_score is not None
                    else 0.0
                ),
                reverse=True,
            )
        else:
            combined_results.sort(
                key=lambda result: result.combined_score,
                reverse=True,
            )

        return combined_results[:k]

    def vector_only_search(
        self,
        query: str,
        k: int = 5,
    ) -> list[dict[str, Any]]:
        return self.vector_store.search(query, k=k)

    def evaluate_query(
        self,
        query: str,
        k: int = 5,
    ) -> dict[str, Any]:
        vector_results = self.vector_only_search(query, k=k)
        hybrid_results = self.search(query, k=k, use_reranker=False)
        reranked_results = self.search(query, k=k, use_reranker=True)

        return {
            "query": query,
            "vector_only": vector_results,
            "bm25_vector": hybrid_results,
            "bm25_vector_reranker": reranked_results,
        }
