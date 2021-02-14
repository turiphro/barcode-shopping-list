from dataclasses import dataclass
from typing import Union
import json


@dataclass
class Item:
    name: str
    description: str
    quantity: int
    info: dict

    def __init__(self, name, description: str = None, quantity: int = 1, info: Union[str, dict] = None, **unknown):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.info = info if isinstance(info, dict) else json.dumps(info)

        if unknown:
            print("[note] ignoring unknown keywords", unknown.keys())
