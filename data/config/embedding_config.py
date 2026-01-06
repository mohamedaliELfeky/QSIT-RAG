from typing import Optional
from pydantic import BaseModel, Field

class RetryConfig(BaseModel):
    max_retries: int
    retry_delay: int
    exponential_backoff: bool


class SparseEmbeddingConfig(BaseModel):
    """Configuration for Sparse Embeddings (e.g., BM25)"""
    enabled: bool = False
    provider: str = "bm25"  # Options: 'bm25', 'splade'
    model_path: Optional[str] = None # Path to tokenizer or model if needed
    modifier: Optional[str] = None  # For specific BM25 variations

class RerankingEmbeddingConfig(BaseModel):
    """Configuration for Late Interaction (ColBERT)"""
    enabled: bool = False
    model_name: str = "colbert-ir/colbertv2.0"
    max_tokens: int = 512  # Max tokens per chunk for ColBERT
    compression_dim: int = 32 # ColBERT compression (usually 32 or 128)


class EmbeddingConfig(BaseModel):
    provider: str
    model: str
    api_key: str
    batch_size: int
    dimensions: int
    retry_config: RetryConfig

    # 2. Hybrid & Late Interaction Extensions
    sparse: SparseEmbeddingConfig = Field(default_factory=SparseEmbeddingConfig)
    colbert: RerankingEmbeddingConfig = Field(default_factory=RerankingEmbeddingConfig)