from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any, Literal

class DataSourceConfig(BaseModel):
    type: Literal["folder", "file", "url", "s3"]
    path: Optional[str] = None
    urls: Optional[List[HttpUrl]] = None
    recursive: bool = False
    file_patterns: List[str] = Field(default_factory=list)
    exclude_patterns: List[str] = Field(default_factory=list)
    crawl_depth: int = 0


class ChunkingStrategy(BaseModel):
    class_: str = Field(alias="class")  # Maps JSON "class" to Python "class_"
    default_params: Dict[str, Any]


class CollectionConfig(BaseModel):
    name: str
    description: str
    data_sources: List[DataSourceConfig]
    chunking_strategy: ChunkingStrategy
    # We allow embedding_override to be None or a dict
    embedding_override: Optional[Dict[str, Any]] = None
    metadata_schema: Dict[str, str]