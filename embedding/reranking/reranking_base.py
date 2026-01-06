from abc import ABC, abstractmethod
from typing import List, Union, Any

# CORRECTED IMPORT: 'base_model' (singular) to match your folder structure
from data.base_model.search_result import VectorSearchResults

# We might want to accept different config types depending on the reranker
from data.config.embedding_config import RerankingEmbeddingConfig
from data.config.query_config import RerankingConfig

class BaseReranker(ABC):
    # Update type hint to be flexible (ColBERT config or generic Reranking config)
    def __init__(self, config: Union[RerankingEmbeddingConfig, RerankingConfig]):
        self.config = config

    @abstractmethod
    def rerank(self, query: str, results: List[VectorSearchResults]) -> List[VectorSearchResults]:
        """
        Accepts a query and a list of initial search results.
        Returns the same list (or subset), re-ordered and re-scored.
        """
        pass