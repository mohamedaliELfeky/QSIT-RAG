import fnmatch
from pathlib import Path
from typing import List
import logging
logger = logging.getLogger(__file__)


from data.config.data_sources_config import DataSourceConfig
from data.base_models.base_models import BaseDocument
from ingestion.readers.file_reader import FileReader

from .base_source import BaseSourceReader



class FolderSourceReader(BaseSourceReader):
    """
    Handles "type": "folder".
    Traverses directories, matches patterns.
    """
    def __init__(self, file_loader:FileReader):
        self.file_loader = file_loader

    def fetch(self, config: DataSourceConfig) -> List[BaseDocument]:
        print(f"--- Scanning Folder: {config.path} ---")
        base_path = Path(config.path)
        
        # 1. Gather all candidate files
        if config.recursive:
            candidates = base_path.rglob("*")
        else:
            candidates = base_path.glob("*")

        # 2. Filter by patterns
        matched_files = []
        for file_path in candidates:
            if not file_path.is_file():
                continue
            
            # Check Include Patterns (e.g., *.pdf)
            if config.file_patterns:
                if not any(fnmatch.fnmatch(file_path.name, pat) for pat in config.file_patterns):
                    continue

            # Check Exclude Patterns (e.g., *temp*)
            if config.exclude_patterns:
                if any(fnmatch.fnmatch(file_path.name, pat) for pat in config.exclude_patterns):
                    continue
            
            matched_files.append(file_path)

        # 3. Use your existing File Loader to actually read them
        # (Assuming your UniversalFileLoader has a read_multiple method)
        return self.file_loader.read_multiple(matched_files)
