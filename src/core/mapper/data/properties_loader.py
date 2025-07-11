import json
from typing import Any, Optional


class JsonProperties:
    _instance: Optional["JsonProperties"] = None
    _json_path = "./properties.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._props = self._load_properties()

    def _load_properties(self) -> dict:
        with open(self._json_path) as properties:
            return json.load(properties)

    def get(self, key: Any, default: Any = "TODO") -> Any:
        return self._props.get(key, default)

    def pop(self, key: Any, default: Any = None) -> Any:
        return self._props.pop(key, default)
