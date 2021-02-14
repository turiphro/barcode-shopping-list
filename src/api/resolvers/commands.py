from supermarktconnector.ah import AHConnector

from .resolver import BaseResolver
from models.item import Item
from exceptions.barcode_not_found_exception import BarcodeNotFoundException


COMMANDS = {
    "list": "LIST",         # for listing list contents
    "add": "ADD",           # for adding products to a list
    "remove": "REMOVE",     # for removing products from a list
}


class CommandResolver(BaseResolver):
    """
    Custom barcode -> command mappings

    These can be useful for clients implementing custom behaviour; for example:
    * scanning 'LIST' command -> expecting one more scan for the name, then calls /lists/ API
    * scanning 'REMOVE' command -> expecting one more scan for a barcode, then removes item from the list
    """
    def __init__(self):
        self.database = None

    def resolve(self, barcode: str) -> (BaseResolver.RESULT_TYPES, Item):

        # TODO: get from DB

        if barcode in COMMANDS:
            name = COMMANDS[barcode]
            return self.RESULT_TYPES.COMMAND.name, Item(name=name)
        else:
            raise BarcodeNotFoundException("No known command called {}".format(barcode))
