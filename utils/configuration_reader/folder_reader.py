import os
import fnmatch
from pathlib import Path
from typing import List, Dict, Any, Union

from .file_reader import FileReader
from .base_source_reader import BaseSourceReader
from data_classes.config.data_sources import DataSourceConfig


class FolderSourceReader(BaseSourceReader):
    """
    Handles "type": "folder".
    Traverses directories, matches patterns.
    """
    def __init__(self, file_loader:FileReader):
        self.file_loader = file_loader

    def fetch(self, config: DataSourceConfig) -> List[Dict[str, Any]]:
        print(f"--- Scanning Folder: {config.path} ---")
        base_path = Path(config.path)
        all_files = []
        
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
