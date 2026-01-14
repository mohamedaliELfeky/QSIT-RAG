import logging
from typing import List

from data_models.base_model.base_models import BaseDocument
from data_models.config.preprocessing_config import PreprocessingConfig
from .intrinsic_extractor import IntrinsicMetadataExtractor
from .base_extractor import BaseMetadataExtractor

logger = logging.getLogger(__name__)

class MetadataProcessor:
    """
    Orchestrates the metadata extraction process.
    Applies Intrinsic (System) extraction followed by any User-Defined extractors.
    """

    def __init__(self, config: PreprocessingConfig, custom_extractors: List[BaseMetadataExtractor] = None):
        # Initialize the System Extractor (Intrinsic)
        regex_configs = config.metadata_extraction.custom_extractors
        self.intrinsic_extractor = IntrinsicMetadataExtractor(regex_configs)
        
        # Store User-Defined Extractors
        self.custom_extractors = custom_extractors or []

    def process(self, documents: List[BaseDocument]) -> List[BaseDocument]:
        logger.info(f"Processing metadata for {len(documents)} documents...")

        for doc in documents:
            # 1. Apply Intrinsic Extraction (File Stats + Regex)
            intrinsic_meta = self.intrinsic_extractor.extract(doc)
            doc.metadata.update(intrinsic_meta)

            # 2. Apply User-Defined Custom Logic
            for extractor in self.custom_extractors:
                try:
                    custom_meta = extractor.extract(doc)
                    if custom_meta:
                        doc.metadata.update(custom_meta)
                except Exception as e:
                    logger.error(f"Custom extractor {extractor.__class__.__name__} failed: {e}")

        return documents