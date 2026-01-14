from abc import ABC, abstractmethod
from typing import Dict, Any
from data_models.base_model.base_models import BaseDocument

class BaseMetadataExtractor(ABC):
    """
    Abstract base class for all metadata extractors.
    User-defined extractors must inherit from this class.
    """

    @abstractmethod
    def extract(self, document: BaseDocument) -> Dict[str, Any]:
        """
        Extract metadata from a document.
        
        Args:
            document: The BaseDocument object.
            
        Returns:
            Dict[str, Any]: A dictionary of metadata to append to the document.
        """
        pass