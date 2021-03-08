from supermarktconnector.ah import AHConnector
import requests

from .resolver import BaseResolver
from models.item import Item


NON_RETRYABLE_CODES = [404]


class AlbertHeijnResolver(BaseResolver):
    def __init__(self):
        self.connector = None
        self.__reconnect__()

    def __reconnect__(self):
        self.connector = AHConnector()

    def resolve(self, barcode: str, retry: int = 1) -> (BaseResolver.RESULT_TYPES, Item):
        while retry >= 0:
            retry -= 1

            try:
                return self.resolve_call(barcode)

            except requests.exceptions.HTTPError as err:
                # retry - incl reconnecting - on issues other than 'not found';
                # by only reconnecting on connection issues, we greatly speed up most lookups
                if any(str(err).startswith(str(status_code))
                       for status_code in NON_RETRYABLE_CODES):
                    raise err

                self.__reconnect__()

    def resolve_call(self, barcode: str, retry: int = 1) -> (BaseResolver.RESULT_TYPES, Item):
        info = self.connector.get_product_by_barcode(barcode)
        print("[OK] AH API returned:", info)

        # seems to be product type/name (without brand etc)
        item = Item(name=info.get('subCategory'),
                    description=info.get("title"),
                    info=info)
        print(f"[->] name={item.name}, description={item.description}")

        return self.RESULT_TYPES.PRODUCT.name, item
