from typing import List
import logging
logger = logging.getLogger(__file__)

from data.config.data_sources_config import DataSourceConfig
from data.base_models.base_models import BaseDocument
from ingestion.readers.file_reader import FileReader

from .base_source import BaseSourceReader


class FileSourceReader(BaseSourceReader):
    """
    Handles "type": "file".
    Reads a specific list of individual files provided in the config.
    """
    def __init__(self, file_loader:FileReader):
        self.file_loader = file_loader

    def fetch(self, config: DataSourceConfig) -> List[BaseDocument]:
       
        target_files = config.path
        print(f"--- Reading Specific Files: {target_files} ---")
        
        
        # 3. Use the Universal Loader
        return self.file_loader.read_file(target_files)
