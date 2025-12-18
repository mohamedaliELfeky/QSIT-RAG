from pydantic import BaseModel

# --- 5. Indexing Config ---
class DeduplicationConfig(BaseModel):
    enabled: bool
    method: str
    similarity_threshold: float

class VersioningConfig(BaseModel):
    enabled: bool
    keep_versions: int

class BatchProcessingConfig(BaseModel):
    batch_size: int
    parallel_workers: int
    rate_limit: int

class IndexingConfig(BaseModel):
    strategy: str
    deduplication: DeduplicationConfig
    versioning: VersioningConfig
    batch_processing: BatchProcessingConfig

