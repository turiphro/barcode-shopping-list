from supermarktconnector.ah import AHConnector

from .resolver import BaseResolver
from models.item import Item
from exceptions.barcode_not_found_exception import BarcodeNotFoundException


COMMANDS = {
    "list": "LIST",             # for changing and displaying the list
    "refresh": "REFRESH",       # for refreshing the list
    "add": "ADD",               # for adding products to a list
    "remove": "REMOVE",         # for removing products from a list
    "1x": "1X", "2x": "2X", "3x": "3X", "4x": "4X",     # quantities
    "exit": "EXIT",             # exit application
    "shutdown": "SHUTDOWN",     # device shutdown
    "update": "UPDATE",         # update application
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
