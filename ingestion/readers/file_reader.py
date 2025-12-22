from pathlib import Path
from typing import List, Dict, Union, Type
import logging
logger = logging.getLogger(__file__)

from data.base_models.base_models import BaseDocument

from .base_reader import BaseFileReader, FallbackReader
from .text_reader import TextReader
from .docx_reader import DocReader
from .image_reader import ImageReader


class FileReader:
    """
    Universal file reader that selects appropriate reader based on file extension.
    """
    _readers:Dict[str, Type[BaseFileReader]] = {
        ".txt":TextReader,
        '.docx':DocReader,
        '.jpg': ImageReader,
        '.png': ImageReader,
        '.jpeg': ImageReader,

    }

    _fall_back_reader = FallbackReader


    def _get_reader(self, extention:str)->BaseFileReader:
        reader = self._readers.get(extention.lower())
        
        if reader:
            return reader()
        return self._fall_back_reader()
    

    def read_file(self, path:Union[Path, str])->BaseDocument:

        obj_path = Path(path)

        if not obj_path.exists():
            logger.warning(f"Warning: File not found: {path}")
            return {}
        
        reader = self._get_reader(obj_path.suffix)

        try:
            content = reader.read(obj_path)

            return content

        except Exception as e:
            logger.error(f"Reading file {path} with error {e}")
            

    def read_multiple(self, paths: List[Union[str, Path]]) -> List[BaseDocument]:
        """Helper to process a list of files."""
        if not paths:
            logger.warning("Warning: List of paths is empty")

        return [self.read_file(p) for p in paths]
    

