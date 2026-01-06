import logging
from typing import List
from openai import OpenAI, OpenAIError

from data.config.embedding_config import EmbeddingConfig
from .dense_base import BaseDenseEmbedding
from ..embedding_factory import register_dense  # Import the decorator

logger = logging.getLogger(__name__)


@register_dense("openai")  # <--- This registers the class automatically
class OpenAIEmbedding(BaseDenseEmbedding):
    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        self.client = OpenAI(api_key=config.api_key)
        self.model = config.model
        self.batch_size = config.batch_size or 100

    def embed_text(self, text: str) -> List[float]:
        # (Same implementation as before...)
        try:
            text = text.replace("\n", " ")
            response = self.client.embeddings.create(input=[text], model=self.model)
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error embedding text: {e}")
            raise e

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        # (Same implementation as before...)
        results = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            batch = [t.replace("\n", " ") for t in batch]
            try:
                response = self.client.embeddings.create(input=batch, model=self.model)
                results.extend([data.embedding for data in response.data])
            except Exception as e:
                logger.error(f"Error embedding batch: {e}")
                raise e
        return results