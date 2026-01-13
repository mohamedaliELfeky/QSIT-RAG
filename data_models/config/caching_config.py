from pydantic import BaseModel

class CacheConfig(BaseModel):
    enabled: bool
    provider: str
    ttl: int
    max_size: str
    embedding_cache: bool
    query_cache: bool

