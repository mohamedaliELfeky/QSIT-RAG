from typing import Union, List, Dict, Any
from pathlib import Path
import logging
import json
logger = logging.getLogger(__file__)

from data_classes.config.rag import RAGConfiguration
from data_classes.config.collection import CollectionConfig

from utils.configuration_reader.collection_reader import CollectionReader
from utils.configuration_reader.file_reader import FileReader


class ConfigLoader:

    def __init__(self, config_path:Union[str, Path]):
        self.config_path:Union[str, Path] = config_path
        self.configuration:RAGConfiguration = None
        self.collection_reader = CollectionReader(FileReader())
    def read_configuration(self)->RAGConfiguration:
        path = Path(self.config_path)
        config_data = {}
        
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found at:{self.config_path}")

        try:
            with open(path, 'r', encoding='utf-8') as file:
                config_data = json.load(file)

        except Exception as e:
            raise ValueError(f"Couldn't parse the configuration file: {e}")

        try:
            self.configuration = RAGConfiguration(**config_data)
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {e}")
    
        return self.configuration
    

    def read_collection(self, collection_name:str=None, collection_index:int=0)->CollectionConfig:
        

    def read_collections(self)->List[CollectionConfig]:
        pass

