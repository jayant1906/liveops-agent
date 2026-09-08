from __future__ import annotations

import math
import re
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from app.retrieval.vector_store import VectorMetadata


@dataclass(frozen=True)
class BM25SearchResult:
    score: float
    metadata: VectorMetadata | dict[str, Any] | None
    text: str


class BM25Retriever:
    def __init__(self, documents: Sequence[str | VectorMetadata | dict[str, Any]]) -> None:
        self.documents = list(documents)
        self.build_index()

    def tokenize(self, text: str) -> list[str]:
        return re.findall(r"\w+", text.lower())

    def build_index(self) -> None:
        self.tokenizedDocs = []
        for doc in self.documents:
            if isinstance(doc, VectorMetadata):
                self.tokenizedDocs.append(self.tokenize(doc.text))
            elif isinstance(doc, dict):
                self.tokenizedDocs.append(self.tokenize(doc.get("text", "")))
            else:
                self.tokenizedDocs.append(self.tokenize(doc))

        self.docLength = [len(tokens) for tokens in self.tokenizedDocs]

        self.docCount = len(self.tokenizedDocs)

        if self.docCount:
            self.avgDocLength = sum(self.docLength) / self.docCount
        else:
            self.avgDocLength = 0.0
        
        self.termFreq = []
        for tokens in self.tokenizedDocs:
            tf = {}
            for token in tokens:
                if token not in tf.keys():
                    tf[token] = 1
                else:
                    tf[token] += 1
            self.termFreq.append(tf)
        
        self.docFreq = defaultdict(int)
        for tokens in self.tokenizedDocs:
            for token in set(tokens):
                self.docFreq[token] += 1

    def search(self, query: str, k: int = 5) -> list[BM25SearchResult]:
        k1 = 1.5
        b = 0.75
        tokenized_query = self.tokenize(query)
        if self.avgDocLength == 0:
            return []
        result = []
        for doc_index, doc in enumerate(self.documents):
            score = 0.0
            for token in tokenized_query:
                tf = self.termFreq[doc_index].get(token, 0)
                if tf:
                    df = self.docFreq[token]
                    idf = math.log((self.docCount - df + 0.5) / (df + 0.5) + 1)

                    numerator = tf * (k1 + 1)
                    denominator = tf + k1 * (
                        1 - b + b * self.docLength[doc_index] / self.avgDocLength
                    )
                    score += idf * numerator / denominator
            if isinstance(doc, VectorMetadata):
                result.append(BM25SearchResult(score=score, metadata=doc, text=doc.text))
            elif isinstance(doc, dict):
                result.append(BM25SearchResult(score=score, metadata = doc, text=doc.get("text", "")))
            elif isinstance(doc, str):
                result.append(BM25SearchResult(score=score, metadata = None, text = doc))
            else:
                pass
        ranked = sorted(result, key=lambda r: r.score, reverse=True)
        return ranked[0:k]
