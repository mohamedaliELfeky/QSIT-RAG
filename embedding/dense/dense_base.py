from abc import ABC, abstractmethod
from typing import List
from data.config.embedding_config import EmbeddingConfig

class BaseDenseEmbedding(ABC):
    def __init__(self, config: EmbeddingConfig):
        self.config = config

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Embed a single string into a dense vector."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of strings into dense vectors."""
        pass

    @property
    def dimension(self) -> int:
        return self.config.dimensions