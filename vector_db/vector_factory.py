import logging
from typing import Dict, Type

from data.config.database_config import DatabaseConfig
from .base import BaseVectorDB

logger = logging.getLogger(__name__)

# 1. The Registry
_VECTOR_DB_REGISTRY: Dict[str, Type[BaseVectorDB]] = {}

def register_vector_db(provider_name: str):
    """
    Decorator to register a Vector DB class.
    Usage: @register_vector_db("qdrant")
    """
    def decorator(cls: Type[BaseVectorDB]):
        _VECTOR_DB_REGISTRY[provider_name.lower()] = cls
        return cls
    return decorator

class VectorDBFactory:
    """
    Factory that uses the dynamic registry to create Vector DB instances.
    """
    @staticmethod
    def create_vector_db(config: DatabaseConfig) -> BaseVectorDB:
        provider = config.provider.lower()
        
        # 2. Dynamic Lookup
        db_cls = _VECTOR_DB_REGISTRY.get(provider)
        
        if not db_cls:
            raise ValueError(
                f"Unsupported vector database provider: '{provider}'. "
                f"Available providers: {list(_VECTOR_DB_REGISTRY.keys())}"
            )
            
        return db_cls(config)