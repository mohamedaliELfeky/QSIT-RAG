from pathlib import Path
from pydantic import BaseModel, Field
from typing import Union, Dict, Any
from enum import Enum




class DistanceMetric(str, Enum):
    COSINE = "Cosine"
    EUCLIDEAN = "Euclidean"
    DOT = "Dot"


class SourceType(str, Enum):
    TXT = "text"
    DOCX = "docx"
    IMAGE = "image"


class BaseDocument(BaseModel):
    """The parent class for all files before chunking."""
    id: str
    source_name: str
    source_path: Union[str, Path]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Each subclass defines its own 'content' type
    source_type: SourceType
