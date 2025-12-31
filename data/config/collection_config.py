from pydantic import BaseModel, Field
from typing import List, Dict, Any

from .data_sources_config import DataSourceConfig
from .chunking_strategy import ChunkingStrategy


class CollectionConfig(BaseModel):
    name: str
    description: str
    data_sources: List[DataSourceConfig]
    chunking_strategy: ChunkingStrategy
    metadata_schema: Dict[str, str]