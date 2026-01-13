import logging
from typing import List

from sentence_transformers import SentenceTransformer
from data_models.config.embedding_config import EmbeddingConfig
from .dense_base import BaseDenseEmbedding
from ..embedding_factory import register_dense

logger = logging.getLogger(__name__)

@register_dense("sentence_transformers")
class SentenceTransformerEmbedding(BaseDenseEmbedding):
    """
    Standard adapter for SentenceTransformers.
    
    Supports models that rely on static prefixes, such as:
    - intfloat/multilingual-e5-large (Needs "query: " and "passage: ")
    - BAAI/bge-m3 (Needs "Represent this sentence..." for queries)
    - standard BERT models (Usually no prefix)
    """
    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        
        logger.info(f"Loading SentenceTransformer model: {config.model}")
        self.model = SentenceTransformer(config.model)
        
        # e.g., "query: " for E5 or "Represent this sentence..." for BGE
        self.query_prefix = config.instruction or ""
        
        # e.g., "passage: " for E5
        self.doc_prefix = config.document_instruction or ""

        if self.query_prefix or self.doc_prefix:
            logger.info(f"Using Prefixes -> Query: '{self.query_prefix}' | Doc: '{self.doc_prefix}'")

    def embed_text(self, text: str) -> List[float]:
        """
        Embeds a single string (treated as a Query).
        Prepends config.instruction if present.
        """
        try:
            text_to_embed = f"{self.query_prefix}{text}"
            return self.model.encode(text_to_embed, convert_to_numpy=True).tolist()
        except Exception as e:
            logger.error(f"Error embedding text: {e}")
            raise e

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a batch of strings (treated as Documents).
        Prepends config.document_instruction if present.
        """
        try:
            # Apply document prefix if defined
            if self.doc_prefix:
                batch_texts = [f"{self.doc_prefix}{t}" for t in texts]
            else:
                batch_texts = texts
            
            embeddings = self.model.encode(
                batch_texts, 
                batch_size=self.batch_size, 
                convert_to_numpy=True,
                show_progress_bar=True
            )
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error embedding batch: {e}")
            raise e