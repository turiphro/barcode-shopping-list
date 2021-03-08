from supermarktconnector.ah import AHConnector

import re

from .resolver import BaseResolver
from models.item import Item
from exceptions.barcode_not_found_exception import BarcodeNotFoundException


REGEX = r"[a-zA-Z0-9- ]*[a-zA-Z]+[a-zA-Z0-9- ]*"


class PlaintextResolver(BaseResolver):
    """
    Plaintext input

    This should *not* match common barcodes (e.g., numbers and dashes only).
    This resolver should be run after CommandResolver (if both are used).
    """
    def resolve(self, barcode: str) -> (BaseResolver.RESULT_TYPES, Item):
        if re.search(REGEX, barcode):
            return self.RESULT_TYPES.PRODUCT.name, Item(name=barcode)
        else:
            raise BarcodeNotFoundException("Input does not match {}: {}".format(REGEX, barcode))
