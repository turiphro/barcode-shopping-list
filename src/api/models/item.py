from dataclasses import dataclass, asdict
from slugify import slugify
from typing import Union
from datetime import datetime
import json


@dataclass
class Item:
    id: str
    name: str
    description: str
    quantity: int
    barcode: str
    resolver: str
    info: dict
    created: str

    def __init__(self, name, description: str = "", id: str = None, quantity: int = 1,
                 barcode: str = None, resolver: str = None, info: Union[str, dict] = None,
                 created: str = None, **unknown):
        self.id = id or slugify(name + " " + description)
        self.name = name
        self.description = description
        self.quantity = quantity
        self.barcode = barcode
        self.resolver = resolver
        self.info = info if isinstance(info, dict) else json.loads(info or "{}")
        self.created = created or datetime.now().isoformat()

        if unknown:
            print("[note] ignoring unknown keywords", unknown.keys())

    def asdict(self):
        d = asdict(self)
        d['info'] = json.dumps(self.info or "{}")
        return d

