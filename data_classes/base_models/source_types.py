from pydantic import BaseModel, Field
from typing import List, Union, Optional, Literal, Dict, Any
from enum import Enum

# --- Shared Components ---

class SourceType(str, Enum):
    TXT = "text"
    DOCX = "docx"
    IMAGE = "image"

# --- Content Structures (The "Meat" of the document) ---

# 1. For DOCX: We need structure (Paragraphs vs Tables)
class DocElement(BaseModel):
    """A single atomic element in a DOCX file."""
    type: Literal["paragraph", "table", "heading"]
    text: str  # The raw text content
    metadata: Dict[str, Any] = {} # e.g., {"bold": True, "level": 1}

class TableElement(DocElement):
    """Special handling for tables so the chunker doesn't break them."""
    type: Literal["table"]
    # List of rows, where each row is a list of cell text
    data: List[List[str]]
    
# 2. For Images: We need visual data + optional extracted text
class ImageContent(BaseModel):
    format: str # png, jpg
    path: str
    # If you ran OCR before chunking, this holds the text.
    # If using Multi-modal embedding (CLIP/GPT-4o), this might be empty.
    ocr_text: Optional[str] = None 


# --- The Main Document Classes ---

class BaseDocument(BaseModel):
    """The parent class for all files before chunking."""
    id: str
    source_path: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Each subclass defines its own 'content' type
    source_type: SourceType

class TextFileDocument(BaseDocument):
    """
    Simple Text File (.txt, .md).
    Content is just one giant string. 
    The chunker will likely split this by character count or newlines.
    """
    source_type: Literal[SourceType.TXT] = SourceType.TXT
    content: str 

class DocxDocument(BaseDocument):
    """
    Structured Document (.docx, .pdf).
    Content is a LIST of elements.
    The chunker can iterate list and decide: "Group these 3 paragraphs, but keep this table whole."
    """
    source_type: Literal[SourceType.DOCX] = SourceType.DOCX
    file_name:str
    content: List[Union[TableElement, DocElement]]

class ImageDocument(BaseDocument):
    """
    Visual File (.png, .jpg).
    Content is the image object.
    The chunker will either chunk the 'ocr_text' OR pass the image path to a Vision Model.
    """
    source_type: Literal[SourceType.IMAGE] = SourceType.IMAGE
    content: ImageContent