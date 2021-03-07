from abc import ABC, abstractmethod
from typing import List

from models.item import Item


class Storage(ABC):
    @abstractmethod
    def get(self, list_name: str) -> List[Item]:
        pass

    @abstractmethod
    def add_item(self, list_name: str, item: Item):
        pass

    @abstractmethod
    def remove_item(self, list_name: str, item_id: str):
        """Removing first occurrence that matches"""
        pass
