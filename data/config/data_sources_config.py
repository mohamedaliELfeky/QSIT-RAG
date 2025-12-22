from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any, Literal


class DataSourceConfig(BaseModel):
    type: Literal["folder", "file", "url", "s3"]
    path: Optional[str] = None
    urls: Optional[List[HttpUrl]] = None
    recursive: bool = False
    file_patterns: List[str] = Field(default_factory=list)
    exclude_patterns: List[str] = Field(default_factory=list)
    crawl_depth: int = 0

