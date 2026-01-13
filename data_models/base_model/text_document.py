from typing import Literal

from .base_models import BaseDocument, SourceType

class TextFileDocument(BaseDocument):
    """
    Simple Text File (.txt, .md).
    Content is just one giant string. 
    The chunker will likely split this by character count or newlines.
    """
    source_type: Literal[SourceType.TXT] = SourceType.TXT
    content: str 
