from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer
from typing import overload, Sequence

from app.config.settings import get_settings


class EmbeddingModel:
    def __init__(
        self,
        model_name: str | None = None,
        device: str | None = None,
        batch_size: int = 64,
    ) -> None:
        settings = get_settings()
        self.model_name = model_name or settings.embedding_model
        self.device = device or settings.embedding_device
        self.batch_size = batch_size
        self.model = SentenceTransformer(self.model_name, device=self.device)

    @overload
    def encode(self, text: str) -> NDArray[np.float32]: ...

    @overload
    def encode(self, text: Sequence[str]) -> NDArray[np.float32]: ...

    def encode(self, text: str | Sequence[str]) -> NDArray[np.float32]:
        embedding = self.model.encode(
            text,
            batch_size=self.batch_size,
            convert_to_numpy=True,
        )
        return np.asarray(embedding, dtype=np.float32)
