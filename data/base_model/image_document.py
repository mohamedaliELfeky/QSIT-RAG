
from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal, Union
from PIL import Image
from .base_models import BaseDocument, SourceType
    

# 2. For Images: We need visual data + optional extracted text
class ImageContent(BaseModel):
    format: str # png, jpg
    # If you ran OCR before chunking, this holds the text.
    # If using Multi-modal embedding (CLIP/GPT-4o), this might be empty.
    ocr_text: Optional[str] = None 



class ImageDocument(BaseDocument):
    """
    Visual File (.png, .jpg).
    Content is the image object.
    The chunker will either chunk the 'ocr_text' OR pass the image path to a Vision Model.
    """
    source_type: Literal[SourceType.IMAGE] = SourceType.IMAGE
    metadata:Union[ImageContent, dict]  # To allow flexibility in metadata
    model_config = ConfigDict(arbitrary_types_allowed=True)

    content: Image