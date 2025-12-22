from pathlib import Path
from typing import Union
from PIL import Image

from data.base_models.image_document import ImageDocument, ImageContent
from .file_reader import BaseFileReader


class ImageReader(BaseFileReader):

    def read(self, image_path:Union[Path, str]) -> ImageDocument:
        img = Image.open(image_path)

        image_content = ImageContent(
            img_format = img.format.lower() if img.format else Path(image_path).suffix.lower().lstrip("."),
            ocr_text=None  # Placeholder; OCR can be added later if needed
        )
        
        return ImageDocument(
                            content=img,
                            metadata=image_content,
                            source_name=Path(image_path).name, 
                            source_path=Path(image_path)
                            )