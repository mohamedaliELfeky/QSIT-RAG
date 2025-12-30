from abc import ABC, abstractmethod

import logging
from typing import List

from data.config.embedding_config import EmbeddingConfig


class BaseEmbedding(ABC):
    def __init__(self, config:EmbeddingConfig):
        self.config = config


    @abstractmethod
    def embed_text(self, text:str) -> List[float]:
        pass

    @abstractmethod
    def embed_batch(self, texts:List[str]) -> List[List[float]]:
        pass

    @property
    def dimension(self) -> int:
        return self.config.dimensions
    

