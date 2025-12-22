from pydantic import BaseModel
from typing import Literal


class ConnectionConfig(BaseModel):
    host: str
    port: int

class DatabaseConfig(BaseModel):
    provider: Literal["qdrant", "pinecone", "weaviate"]
    connection: ConnectionConfig