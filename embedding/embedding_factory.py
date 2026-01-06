from typing import Dict, Type, Any, Optional
from data.config.embedding_config import EmbeddingConfig

# Import the new Base classes
from .dense.dense_base import BaseDenseEmbedding
from .sparse.sparse_base import BaseSparseEmbedding
from .reranking.reranking_base import BaseReranker

# Registries for each type
_DENSE_REGISTRY: Dict[str, Type[BaseDenseEmbedding]] = {}
_SPARSE_REGISTRY: Dict[str, Type[BaseSparseEmbedding]] = {}
_RERANK_REGISTRY: Dict[str, Type[BaseReranker]] = {}

# --- Registration Decorators ---

def register_dense(provider_name: str):
    def decorator(cls: Type[BaseDenseEmbedding]):
        _DENSE_REGISTRY[provider_name.lower()] = cls
        return cls
    return decorator

def register_sparse(provider_name: str):
    def decorator(cls: Type[BaseSparseEmbedding]):
        _SPARSE_REGISTRY[provider_name.lower()] = cls
        return cls
    return decorator

def register_reranker(provider_name: str):
    def decorator(cls: Type[BaseReranker]):
        _RERANK_REGISTRY[provider_name.lower()] = cls
        return cls
    return decorator


# --- The Factory ---

class EmbeddingFactory:
    """
    Factory to retrieve specific embedding or reranking models.
    """

    @staticmethod
    def get_dense_model(config: EmbeddingConfig) -> BaseDenseEmbedding:
        provider = config.provider.lower()
        model_cls = _DENSE_REGISTRY.get(provider)
        if not model_cls:
            raise ValueError(f"Dense provider '{provider}' not found. Options: {list(_DENSE_REGISTRY.keys())}")
        return model_cls(config)

    @staticmethod
    def get_sparse_model(config: EmbeddingConfig) -> BaseSparseEmbedding:
        # Assuming the config has a 'sparse' sub-config as defined in previous steps
        if not config.sparse.enabled:
            raise ValueError("Sparse embedding is not enabled in configuration.")
            
        provider = config.sparse.provider.lower()
        model_cls = _SPARSE_REGISTRY.get(provider)
        if not model_cls:
            raise ValueError(f"Sparse provider '{provider}' not found. Options: {list(_SPARSE_REGISTRY.keys())}")
        return model_cls(config.sparse)

    @staticmethod
    def get_reranking_model(config: EmbeddingConfig) -> BaseReranker:
        # This handles ColBERT or other rerankers defined in the embedding config
        if not config.colbert.enabled:
             raise ValueError("ColBERT/Reranking is not enabled in embedding configuration.")

        # For now, we assume 'colbert' is the key, but this can be dynamic like the others
        model_cls = _RERANK_REGISTRY.get("colbert") 
        if not model_cls:
            raise ValueError("ColBERT model not registered.")
        return model_cls(config.colbert)