from typing import List, Dict, Any

from abc import ABC, abstractmethod

from data.config.data_sources_config import DataSourceConfig

class BaseSourceReader(ABC):

    @abstractmethod
    def fetch(self, config:DataSourceConfig) -> List[Dict[str, Any]]:
        pass

