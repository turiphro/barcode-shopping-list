from supermarktconnector.ah import AHConnector

from .resolver import BaseResolver
from models.item import Item


class AlbertHeijnResolver(BaseResolver):
    def __init__(self):
        self.connector = None
        self.__reconnect__()

    def __reconnect__(self):
        self.connector = AHConnector()

    def resolve(self, barcode: str) -> (BaseResolver.RESULT_TYPES, Item):
        self.__reconnect__()  # prevent timeouts

        info = self.connector.get_product_by_barcode(barcode)
        print("[OK] AH API returned:", info)

        # seems to be product type/name (without brand etc)
        item = Item(name=info.get('subCategory'),
                    description=info.get("title"),
                    info=info)
        print(f"[->] name={item.name}, description={item.description}")

        return self.RESULT_TYPES.PRODUCT.name, item
