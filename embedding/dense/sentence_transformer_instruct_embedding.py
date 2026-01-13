import logging
from typing import List
from sentence_transformers import SentenceTransformer
from data_models.config.embedding_config import EmbeddingConfig
from .dense_base import BaseDenseEmbedding
from ..embedding_factory import register_dense

logger = logging.getLogger(__name__)

@register_dense("sentence_transformers_instruct")
class SentenceTransformerInstructEmbedding(BaseDenseEmbedding):
    """
    Specialized adapter for Instruct-tuned models (E5-Instruct, Instructor-XL).
    Instructions are now fully configurable via EmbeddingConfig.
    """
    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        
        logger.info(f"Loading Instruct-tuned model: {config.model}")
        self.model = SentenceTransformer(config.model)
        
        # 1. Load Query Instruction (Default to E5 format if not provided)
        if config.instruction:
            self.query_instruction = config.instruction
        else:
            # Fallback default for E5-Instruct
            self.query_instruction = "Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery: "
            logger.info(f"No instruction provided in config. Using default: '{self.query_instruction.strip()}'")

        # 2. Load Document Instruction (Default to None/Empty)
        self.doc_instruction = config.document_instruction or ""

    def embed_text(self, text: str) -> List[float]:
        """
        Embeds a QUERY.
        """
        try:
            # Combine instruction + query text
            # E.g. "Instruct: ... \nQuery: " + "what is python?"
            formatted_text = f"{self.query_instruction}{text}"
            return self.model.encode(formatted_text, convert_to_numpy=True).tolist()
        except Exception as e:
            logger.error(f"Error embedding query: {e}")
            raise e

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds DOCUMENTS.
        """
        try:
            # Apply document instruction if it exists (Needed for 'Instructor-XL', ignored for 'E5')
            if self.doc_instruction:
                batch_texts = [f"{self.doc_instruction}{t}" for t in texts]
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
            logger.error(f"Error embedding document batch: {e}")
            raise e