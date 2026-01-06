from abc import ABC, abstractmethod
from typing import List, Dict, Any
from data.config.embedding_config import SparseEmbeddingConfig

# Qdrant and others usually expect sparse vectors as a dict of indices and values
# e.g., {"indices": [10, 20], "values": [0.5, 0.8]}
class BaseSparseEmbedding(ABC):
    def __init__(self, config: SparseEmbeddingConfig):
        self.config = config

    @abstractmethod
    def embed_text(self, text: str) -> Dict[str, List[Any]]:
        """
        Returns a sparse vector representation.
        Format example: {'indices': [123, 456], 'values': [0.1, 0.9]}
        """
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[Dict[str, List[Any]]]:
        """Batch processing for sparse embeddings."""
        pass