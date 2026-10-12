from __future__ import annotations

from collections.abc import Sequence

from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        device: str | None = None,
    ) -> None:
        self.model = CrossEncoder(model_name, device=device)

    def predict(self, pairs: Sequence[Sequence[str]]) -> list[float]:
        if not pairs:
            return []

        scores = self.model.predict(pairs)
        return [float(score) for score in scores]
