import os
from pathlib import Path
import logging

logger = logging.getLogger(__file__)

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel

from data.base_models.search_result import VectorSearchResults
from data.base_models.base_models import DistanceMetric

class BaseVectorDB(ABC):

    @abstractmethod
    def create_collection(self, collection_name:str, vector_size:int, distance:DistanceMetric=DistanceMetric.COSINE):
        """Create a collectoin if doesn't exist."""
        pass

    @abstractmethod
    def insert(self, collection_name:str, vectors:List[List[float]], metadata:List[Dict[str, Any]], ids:Optional[List[str]]=None):
        pass


    @abstractmethod
    def search(self, collection_name:str, query_vector:List[float], limit:int=5, fliters:Optional[Dict]=None) -> VectorSearchResults:
        pass

    @abstractmethod
    def delete(self, collection_name:str, document_id:str):
        pass

