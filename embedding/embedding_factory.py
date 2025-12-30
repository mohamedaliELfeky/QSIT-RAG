from typing import Dict, Type, Any
from data.config.embedding_config import EmbeddingConfig
from .base import BaseEmbedding

# 1. The Registry
_EMBEDDING_REGISTRY: Dict[str, Type[BaseEmbedding]] = {}

def register_embedding(provider_name: str):
    """
    Decorator to register an embedding class.
    Usage: @register_embedding("openai")
    """
    def decorator(cls: Type[BaseEmbedding]):
        _EMBEDDING_REGISTRY[provider_name.lower()] = cls
        return cls
    return decorator

class EmbeddingFactory:
    """
    Factory that uses the dynamic registry.
    """
    @staticmethod
    def get_embedding_model(config: EmbeddingConfig) -> BaseEmbedding:
        provider = config.provider.lower()
        
        # 2. Dynamic Lookup
        embedding_cls = _EMBEDDING_REGISTRY.get(provider)
        
        if not embedding_cls:
            raise ValueError(
                f"Unsupported embedding provider: '{provider}'. "
                f"Available providers: {list(_EMBEDDING_REGISTRY.keys())}"
            )
            
        return embedding_cls(config)