from dataclasses import dataclass


@dataclass
class Item:
    name: str
    description: str = None
    quantity: int = 1
    info: dict = None
