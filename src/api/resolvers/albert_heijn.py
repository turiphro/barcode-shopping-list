from supermarktconnector import ah
import requests

from .resolver import BaseResolver
from models.item import Item


NON_RETRYABLE_CODES = [404]


class AlbertHeijnResolver(BaseResolver):
    def __init__(self):
        self.connector = None
        self.__reconnect__()

    def __reconnect__(self):
        #ah.HEADERS = {
        #    'Host': 'api.ah.nl',
        #    'content-type': 'application/json; charset=UTF-8',
        #    'user-agent': 'HTTPie/3.2.2',
        #}
        self.connector = ah.AHConnector()

    def resolve(self, barcode: str, retry: int = 1) -> (BaseResolver.RESULT_TYPES, Item):
        while retry >= 0:
            retry -= 1

            try:
                return self.resolve_call(barcode)

            except requests.exceptions.HTTPError as err:
                # retry - incl reconnecting - on issues other than 'not found';
                # by only reconnecting on connection issues, we greatly speed up most lookups
                print("[ERR] Exception from the AH API:", err)
                if any(str(err).startswith(str(status_code))
                       for status_code in NON_RETRYABLE_CODES):
                    raise err

                self.__reconnect__()

    def resolve_call(self, barcode: str, retry: int = 1) -> (BaseResolver.RESULT_TYPES, Item):
        info = self.connector.get_product_by_barcode(barcode)
        print("[OK] AH API returned:", info)

        item = Item(name=info.get('subCategory'),
                    description=info.get("title"),
                    info=info)
        print(f"[->] name={item.name}, description={item.description}")

        return self.RESULT_TYPES.PRODUCT.name, item
