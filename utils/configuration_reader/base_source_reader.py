import os
from pathlib import Path
from typing import List, Dict, Any, Union

from abc import ABC, abstractmethod

from data_classes.config.data_sources import DataSourceConfig


class BaseSourceReader(ABC):

    @abstractmethod
    def fetch(self, config:DataSourceConfig) -> List[Dict[str, Any]]:
        pass

