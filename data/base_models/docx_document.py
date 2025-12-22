from pydantic import BaseModel
from typing import List, Union, Literal, Dict, Any
from .base_models import BaseDocument, SourceType


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


class DocxDocument(BaseDocument):
    """
    Structured Document (.docx, .pdf).
    Content is a LIST of elements.
    The chunker can iterate list and decide: "Group these 3 paragraphs, but keep this table whole."
    """
    source_type: Literal[SourceType.DOCX] = SourceType.DOCX
    content: List[Union[TableElement, DocElement]]
