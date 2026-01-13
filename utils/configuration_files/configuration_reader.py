import json
import os
import re
from typing import Any

from data_models.config.rag_config import RAGConfiguration

class ConfigurationReader:
    @staticmethod
    def _expand_env_vars(data: Any) -> Any:
        """Recursively replaces ${VAR} with environment variable values."""
        if isinstance(data, dict):
            return {k: ConfigurationReader._expand_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [ConfigurationReader._expand_env_vars(i) for i in data]
        elif isinstance(data, str):
            match = re.search(r"\$\{(\w+)\}", data)
            if match:
                return os.getenv(match.group(1), data)
        return data
    

    @staticmethod
    def load_config(path: str) -> RAGConfiguration:
        """Loads and validates the master configuration."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config not found at: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)

        expanded = ConfigurationReader._expand_env_vars(config_dict)
        return RAGConfiguration(**expanded)