from abc import ABC, abstractmethod
import logging

from pathlib import Path
from typing import List, Dict, Any, Union, Type

from PIL import Image

from .document_reader import WordDocument, read_word_file
from data_classes.config.data_sources import DataSourceConfig
from .base_source_reader import BaseSourceReader


logger = logging.getLogger(__file__)

class BaseFileReader(ABC):

    @abstractmethod
    def read(self, file_path:Union[Path, str]):
        pass


class TextReader(BaseFileReader):

    def read(self, txt_path:Union[Path, str]):
        content = None
        with open(txt_path, 'r') as file:
            content = file.read()

        return content


class ImageReader(BaseFileReader):

    def read(self, image_path:Union[Path, str]) -> Image:
        return Image.open(image_path)


class DocReader(BaseFileReader):
    def read(self, doc_path:Union[Path, str]) -> WordDocument:
        return read_word_file(doc_path)


class FallbackReader(BaseFileReader):
    """Handles unknown file types gracefully."""
    def read(self, file_path: Path) -> str:
        return f"Binary/Unknown content for {file_path.name}"
    

class FileReader:
    
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
    

    def read_file(self, path:Union[Path, str])->Dict[str, Any]:

        obj_path = Path(path)

        if not obj_path.exists():
            logger.warning(f"Warning: File not found: {path}")
            return {}
        
        reader = self._get_reader(obj_path.suffix)

        try:
            content = reader.read(obj_path)

            return {
                "filename":obj_path.name,
                "path": str(obj_path.absolute()),
                "content":content
            }
        
        except Exception as e:
            logger.error(f"Reading file {path} with error {e}")
            

    def read_multiple(self, paths: List[Union[str, Path]]) -> List[Dict[str, Any]]:
        """Helper to process a list of files."""
        if not paths:
            logger.warning("Warning: List of paths is empty")

        return [self.read_file(p) for p in paths]
    

class FileSourceReader(BaseSourceReader):
    """
    Handles "type": "file".
    Reads a specific list of individual files provided in the config.
    """
    def __init__(self, file_loader:FileReader):
        self.file_loader = file_loader

    def fetch(self, config: DataSourceConfig) -> List[Dict[str, Any]]:
       
        target_files = config.path
        print(f"--- Reading Specific Files: {target_files} ---")
        
        
        # 3. Use the Universal Loader
        return self.file_loader.read_file(target_files)
