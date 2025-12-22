from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path


class BaseFileReader(ABC):

    @abstractmethod
    def read(self, file_path:Union[Path, str]):
        pass


class FallbackReader(BaseFileReader):
    """Handles unknown file types gracefully."""
    def read(self, file_path: Path) -> str:
        return f"Binary/Unknown content for {file_path.name}"
    
