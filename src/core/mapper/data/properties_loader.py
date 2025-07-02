import json
from typing import Any, Optional

class JsonProperties:
    _props: Optional[dict] = None
    _json_path = "./properties.json"

    def __new__(cls):
        if cls._props:
            return cls._props
        return super().__new__(cls)

    def __init__(self):
        self._props = json.load(open(self._json_path))

    def get(self, key: Any, default: Any) -> Any:
        return self._props.get(key, default)
    
    def pop(self, key: Any, default: Any) -> Any:
        return self._props.pop(key, default)