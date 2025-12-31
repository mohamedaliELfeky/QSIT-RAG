from pydantic import BaseModel, Field
from typing import Dict, Any

class Chunk(BaseModel):
    """Represents a chunk of data with associated document"""

    id: str = Field(..., description="Unique identifier for the chunk.")
    document_id: str = Field(..., description="ID of the parent document.")
    content: str = Field(..., description="The actual text content.")
    index: int = Field(..., description="Order of the chunk in the document.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional information with the chunk.")


    class Config:
        arbitrary_types_allowed = True


