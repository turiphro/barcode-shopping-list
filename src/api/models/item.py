from dataclasses import dataclass, asdict
from typing import Union
import json


@dataclass
class Item:
    name: str
    description: str
    quantity: int
    barcode: str
    info: dict

    def __init__(self, name, description: str = None, quantity: int = 1,
                 barcode: str = None, info: Union[str, dict] = None, **unknown):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.barcode = barcode
        self.info = info if isinstance(info, dict) else json.loads(info or "{}")

        if unknown:
            print("[note] ignoring unknown keywords", unknown.keys())

    def asdict(self):
        d = asdict(self)
        d['info'] = json.dumps(self.info or "{}")
        return d

