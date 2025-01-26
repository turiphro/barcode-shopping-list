from supermarktconnector.jumbo import JumboConnector
import requests

from .resolver import BaseResolver
from models.item import Item
from exceptions.barcode_not_found_exception import BarcodeNotFoundException

NON_RETRYABLE_CODES = [404]


class JumboResolver(BaseResolver):
    def __init__(self):
        self.connector = None
        self.__reconnect__()

    def __reconnect__(self):
        self.connector = JumboConnector()

    def resolve(self, barcode: str, retry: int = 1) -> (BaseResolver.RESULT_TYPES, Item):
        while retry >= 0:
            retry -= 1

            try:
                return self.resolve_call(barcode)

            except requests.exceptions.HTTPError as err:
                # retry - incl reconnecting - on issues other than 'not found';
                # by only reconnecting on connection issues, we greatly speed up most lookups
                print("[ERR] Exception from the Jumbo API:", err)
                if any(str(err).startswith(str(status_code))
                       for status_code in NON_RETRYABLE_CODES):
                    raise err

                self.__reconnect__()

    def resolve_call(self, barcode: str, retry: int = 1) -> (BaseResolver.RESULT_TYPES, Item):
        info = self.connector.get_product_by_barcode(barcode)

        if not info:
            raise BarcodeNotFoundException("Jumbo API returned no products")

        print("[OK] Jumbo API returned:", info)

        # more details can be obtained with a second call:
        details = self.connector.get_product_details(info) \
            .get('product', {}) \
            .get('data')
        print("details:", details)

        item = Item(name=details.get('regulatedTitle') or info.get('title'),
                    description=details.get('title'),
                    info=details or info)
        print(f"[->] name={item.name}, description={item.description}")

        return self.RESULT_TYPES.PRODUCT.name, item
