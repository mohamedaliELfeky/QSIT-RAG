import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from data_models.base_model.base_models import BaseDocument
from data_models.base_model.metadata_enums import IntrinsicMetadataType
from data_models.config.preprocessing_config import MetadataExtractorConfig
from .base_extractor import BaseMetadataExtractor

logger = logging.getLogger(__name__)

class IntrinsicMetadataExtractor(BaseMetadataExtractor):
    """
    Built-in extractor for:
    1. File System attributes (Size, Date, Name).
    2. Config-driven Regex patterns.
    """

    def __init__(self, regex_configs: Optional[List[MetadataExtractorConfig]] = None):
        self._regex_patterns = {}
        if regex_configs:
            for config in regex_configs:
                try:
                    self._regex_patterns[config.name] = re.compile(config.pattern)
                except re.error as e:
                    logger.error(f"Invalid Regex pattern for '{config.name}': {e}")

    def extract(self, document: BaseDocument) -> Dict[str, Any]:
        meta = {}
        
        # 1. File System Stats
        self._extract_filesystem_stats(document, meta)
        
        # 2. Regex Pattern Matching
        if hasattr(document, 'content') and document.content:
            self._apply_regex_patterns(document.content, meta)
            
        return meta

    def _extract_filesystem_stats(self, doc: BaseDocument, meta: Dict[str, Any]):
        path_str = str(doc.source_path)
        try:
            path_obj = Path(path_str)
            if path_obj.exists():
                stats = path_obj.stat()
                meta[IntrinsicMetadataType.FILE_SIZE.value] = stats.st_size
                meta[IntrinsicMetadataType.FILE_EXTENSION.value] = path_obj.suffix.lower()
                meta[IntrinsicMetadataType.CREATION_DATE.value] = datetime.fromtimestamp(stats.st_ctime).isoformat()
                meta[IntrinsicMetadataType.LAST_MODIFIED.value] = datetime.fromtimestamp(stats.st_mtime).isoformat()
                meta[IntrinsicMetadataType.FILE_NAME.value] = path_obj.name
        except Exception as e:
            logger.warning(f"Failed to extract intrinsic stats for {doc.source_name}: {e}")

    def _apply_regex_patterns(self, content: str, meta: Dict[str, Any]):
        for name, pattern in self._regex_patterns.items():
            match = pattern.search(content)
            if match:
                meta[name] = match.group(0)