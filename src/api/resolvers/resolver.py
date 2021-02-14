from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any

from models.item import Item


class BaseResolver(ABC):
    RESULT_TYPES = Enum("TYPES", "PRODUCT COMMAND")

    @abstractmethod
    def resolve(self, barcode: str) -> (RESULT_TYPES, Item):
        pass
