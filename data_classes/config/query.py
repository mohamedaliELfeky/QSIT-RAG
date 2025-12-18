from pydantic import BaseModel
from typing import List

# --- 6. Query Config ---
class HybridSearchConfig(BaseModel):
    enabled: bool
    alpha: float
    keyword_weight: float
    semantic_weight: float

class RerankingConfig(BaseModel):
    enabled: bool
    model: str
    top_n: int

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
