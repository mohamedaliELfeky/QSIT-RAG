from pydantic import BaseModel
from typing import List

# --- 6. Query Config ---

class HybridSearchConfig(BaseModel):
    enabled: bool
    # Weights for Reciprocal Rank Fusion (RRF) or Linear combination
    dense_weight: float = 0.5
    sparse_weight: float = 0.5
    colbert_weight: float = 0.0 # If ColBERT is used purely for reranking, this might be 0 during initial fetch
    
    # Thresholds
    minimum_score: float = 0.0

class RerankingConfig(BaseModel):
    enabled: bool = True  # Defaults to True as per your requirement
    provider: str = "cross-encoder" # 'cross-encoder' or 'colbert' (if used as reranker only)
    model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    top_n: int = 5  # How many documents to send to the reranker

class DateRangeConfig(BaseModel):
    enabled: bool
    default_days: int

class FiltersConfig(BaseModel):
    metadata_filters: List[str]
    date_range: DateRangeConfig

class QueryConfig(BaseModel):
    default_top_k: int
    similarity_threshold: float
    hybrid_search: HybridSearchConfig
    reranking: RerankingConfig
    filters: FiltersConfig