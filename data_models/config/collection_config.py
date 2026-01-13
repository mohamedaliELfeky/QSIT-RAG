from pydantic import BaseModel, Field
from typing import List, Dict, Any

from .data_sources_config import DataSourceConfig
from .chunking_strategy import ChunkingStrategy


class VectorSettings(BaseModel):

    use_dense:bool = True
    use_sparse:bool = True
    use_rerank:bool = True

class CollectionConfig(BaseModel):
    name: str
    description: str
    data_sources: List[DataSourceConfig]
    chunking_strategy: ChunkingStrategy
    metadata_schema: Dict[str, str]
    vector_settings: VectorSettings = Field(default_factory=VectorSettings)
