from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class VectorSearchResults(BaseModel):

    id:str
    score:float
    content:Optional[str] = None
    metadata:Dict[str, Any] = Field(default=dict)


