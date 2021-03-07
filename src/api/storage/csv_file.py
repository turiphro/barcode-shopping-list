import os
from csv import DictReader, DictWriter
from typing import List

from .storage import Storage
from models.item import Item


class CsvFile(Storage):
    # Note: this is a naive implementation, without
    # taking care of race conditions (read/write locks etc)

    def __init__(self, folder: str):
        self.folder = folder

    def __get_list_items__(self, list_name: str) -> List[Item]:
        filepath = os.path.join(self.folder, f"{list_name}.csv")
        if os.path.exists(filepath):
            with open(filepath) as item_fp:
                reader = DictReader(item_fp)
                return list(Item(**row) for row in reader)
        else:
            return []

    def __save_list__(self, list_name: str, items: List[Item]):
        filepath = os.path.join(self.folder, f"{list_name}.csv")

        if len(items) == 0:
            if os.path.exists(filepath):
                os.remove(filepath)  # remove file if there are no items
            return

        fieldnames = items[0].asdict().keys()
        with open(filepath, "w") as item_fp:
            writer = DictWriter(item_fp, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow(item.asdict())

    def get(self, list_name: str) -> List[Item]:
        return self.__get_list_items__(list_name)

    def add_item(self, list_name: str, item: Item):
        items = self.__get_list_items__(list_name)
        items.append(item)
        self.__save_list__(list_name, items)

    def remove_item(self, list_name: str, list_id: str):
        items = self.__get_list_items__(list_name)
        for item in items:
            if item.id == list_id:
                items.remove(item)
                break
        self.__save_list__(list_name, items)
