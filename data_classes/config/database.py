from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any, Literal


class ConnectionConfig(BaseModel):
    host: str
    port: int

class DatabaseConfig(BaseModel):
    provider: Literal["qdrant", "pinecone", "weaviate"]
    connection: ConnectionConfig