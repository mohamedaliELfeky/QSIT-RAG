from pydantic import BaseModel
from typing import List 
import json

from .database import DatabaseConfig
from .collection import CollectionConfig
from .embedding import EmbeddingConfig
from .preprocessing import PreprocessingConfig
from .indexing import IndexingConfig
from .query import QueryConfig
from .monitoring import MonitoringConfig
from .caching import CacheConfig




# --- 8. Master Configuration ---
class RAGConfiguration(BaseModel):
    database: DatabaseConfig
    collections: List[CollectionConfig]
    embedding: EmbeddingConfig
    preprocessing: PreprocessingConfig
    indexing: IndexingConfig
    query: QueryConfig
    monitoring: MonitoringConfig
    cache: CacheConfig


# --- Usage Example ---
if __name__ == "__main__":
    # Simulate reading the JSON file
    # In a real scenario: with open('config.json') as f: config_data = json.load(f)
    json_path = r"D:\Projects and POCs\RAG for everyone\qsit_rag\config.json"
    # Using the raw JSON string you provided earlier for demonstration
    with open(json_path, 'r') as file:
        
      json_str = file.read()


    try:
        # 1. Parse JSON
        raw_config = json.loads(json_str)
        
        # 2. Validate with Pydantic
        rag_config = RAGConfiguration(**raw_config)
        
        print("✅ Configuration Validated Successfully!")
        print(f"Database Provider: {rag_config.database.provider}")
        print(f"Embedding Model: {rag_config.embedding.model}")
        print(f"Chunking Strategy: {rag_config.collections[0].chunking_strategy.class_}")
        
    except Exception as e:
        print(f"❌ Configuration Error: {e}")