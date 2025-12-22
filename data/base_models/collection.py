from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from data.base_models.base_models import BaseDocument
from data.config.collection_config import ChunkingStrategy
from data.config.embedding_config import EmbeddingConfig


class Collection(BaseModel):
    """
    Runtime representation of a collection.
    Built from CollectionConfig + ingestion output.
    """

    name: str
    description: Optional[str] = None

    documents: List[BaseDocument] = Field(default_factory=list)

    # Metadata rules (used later for validation / filtering)
    metadata_schema: Dict[str, Any] = Field(default_factory=dict)

    # Strategy names, NOT implementations
    chunking_strategy: Optional[ChunkingStrategy] = None
    embedding_override: Optional[EmbeddingConfig] = None

    @property
    def size(self) -> int:
        return len(self.documents)
