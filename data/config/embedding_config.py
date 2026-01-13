from typing import Optional
from pydantic import BaseModel, Field

class RetryConfig(BaseModel):
    max_retries: int
    retry_delay: int
    exponential_backoff: bool

class SparseEmbeddingConfig(BaseModel):
    """Configuration for Sparse Embeddings (e.g., BM25)"""
    enabled: bool = False
    provider: str = "bm25"
    model_path: Optional[str] = None
    modifier: Optional[str] = None

class RerankingEmbeddingConfig(BaseModel):
    """Configuration for Late Interaction (ColBERT)"""
    enabled: bool = False
    model_name: str = "colbert-ir/colbertv2.0"
    max_tokens: int = 512
    compression_dim: int = 32

class EmbeddingConfig(BaseModel):
    provider: str
    model: str
    api_key: str
    batch_size: int
    dimensions: int
    retry_config: RetryConfig

    # Default instruction for Queries (used by E5-Instruct, Instructor-XL, etc.)
    instruction: Optional[str] = None 
    # Optional instruction for Documents (used by Instructor-XL, usually None for E5)
    document_instruction: Optional[str] = None

    # 2. Hybrid & Late Interaction Extensions
    sparse: SparseEmbeddingConfig = Field(default_factory=SparseEmbeddingConfig)
    colbert: RerankingEmbeddingConfig = Field(default_factory=RerankingEmbeddingConfig)