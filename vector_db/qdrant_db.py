import os
from pathlib import Path
from typing import List, Dict, Optional, Any
import uuid
import logging

logger = logging.getLogger(__file__)

from qdrant_client import QdrantClient, models

from data.base_models.base_models import DistanceMetric
from data.config.database_config import DatabaseConfig
from data.base_models.search_result import VectorSearchResults
from .base import BaseVectorDB
from .vector_factory import register_vector_db

@register_vector_db("qdrant")  # <--- Self-registration
class QdrantDB(BaseVectorDB):
    _DISTANCE_MAP = {
        DistanceMetric.COSINE: models.Distance.COSINE,
        DistanceMetric.EUCLIDEAN: models.Distance.EUCLID,
        DistanceMetric.DOT: models.Distance.DOT,
    }

    def __init__(self, config:DatabaseConfig):
        self.host = config.connection.host
        self.port = config.connection.port

        self.client = QdrantClient(host=self.host, port=self.port)

    
    def create_collection(self, collection_name, vector_size, distance = DistanceMetric.COSINE):
        qdrant_distance = self._DISTANCE_MAP.get(distance, DistanceMetric.COSINE)

        if not self.client.collection_exists(collection_name=collection_name):
            self.client.create_collection(
                                collection_name=collection_name,
                                vectors_config=models.VectorParams(
                                    size=vector_size,
                                    distance=qdrant_distance
                                )
                            )
            
    
    def insert(self, collection_name, vectors, metadata, ids = None):
        if ids is None:

            ids = [str(uuid.uuid4()) for _ in range(len(vectors))]

        points = [
            models.PointStruct(id=idx, vector=vector, payload=meta)
            for idx, vector, meta in zip(ids, vectors, metadata)
        ]

        self.client.upsert(collection_name=collection_name, points=points)

    def _build_qdrant_filter(self, filters: Dict[str, Any]) -> Optional[models.Filter]:
        """
        Converts a simple dictionary of key-value pairs into a Qdrant Filter model.
        Supports exact matches for single values and 'any' matches for lists.
        """
        if not filters:
            return None

        conditions = []
        for key, value in filters.items():
            if isinstance(value, list):
                # If value is a list, match ANY of the values (OR logic within the field)
                conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchAny(any=value)
                    )
                )
            else:
                # Exact match for single values
                conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    )
                )

        # We wrap all conditions in a 'must' clause (AND logic between fields)
        return models.Filter(must=conditions)
    

    def search(self, collection_name, query_vector, limit = 5, fliters = None) -> VectorSearchResults:

        qdrant_filter = self._build_qdrant_filter(fliters)

        search_results = self.client.query_points(
                                            collection_name=collection_name, 
                                            query=query_vector,
                                            query_filter=qdrant_filter,
                                            limit=limit
                                        ).points
        
        results:List[VectorSearchResults] = list()
        for point in search_results:

            content = point.payload.get('text', point.payload.get("content", "")) if point.payload else ""

            results.append(VectorSearchResults(
                id=str(point.id),
                score=point.score,
                content=content,
                metadata=point.payload if point.payload else {}
            ))

        
        return results
    

    def delete(self, collection_name, document_id):
        self.client.delete(
                collection_name=collection_name,
                points_selector=models.PointsSelector(points=[document_id])
            )
        
    