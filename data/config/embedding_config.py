from pydantic import BaseModel

class RetryConfig(BaseModel):
    max_retries: int
    retry_delay: int
    exponential_backoff: bool

class EmbeddingConfig(BaseModel):
    provider: str
    model: str
    api_key: str
    batch_size: int
    dimensions: int
    retry_config: RetryConfig