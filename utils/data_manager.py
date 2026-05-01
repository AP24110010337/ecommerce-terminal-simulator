import json
import os
from typing import Any, Dict, List

DATA_DIR = "data"

class DataManager:
    """Manages secure read/write operations for file-based JSON storage."""
    
    @staticmethod
    def _get_filepath(filename: str) -> str:
        return os.path.join(DATA_DIR, filename)
    
    @classmethod
    def ensure_file_exists(cls, filename: str, default_data: Any = None):
        """Creates the JSON file if it doesn't already exist."""
        if default_data is None:
            default_data = {}
            
        filepath = cls._get_filepath(filename)
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(filepath):
            cls.save_data(filename, default_data)

    @classmethod
    def load_data(cls, filename: str) -> Any:
        """Loads and returns data from a JSON file."""
        filepath = cls._get_filepath(filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @classmethod
    def save_data(cls, filename: str, data: Any) -> None:
        """Saves data dict/list to a JSON file safely."""
        filepath = cls._get_filepath(filename)
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
