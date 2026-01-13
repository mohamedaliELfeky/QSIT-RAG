from pydantic import BaseModel

# --- 7. Monitoring & Cache Config ---
class LoggingConfig(BaseModel):
    level: str
    file: str
    rotation: str

class MetricsConfig(BaseModel):
    track_embeddings: bool
    track_queries: bool
    track_latency: bool

class MonitoringConfig(BaseModel):
    logging: LoggingConfig
    metrics: MetricsConfig
