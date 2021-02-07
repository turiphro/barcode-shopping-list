from supermarktconnector.ah import AHConnector

from .resolver import BaseResolver


class AlbertHeijnResolver(BaseResolver):
    def __init__(self):
        self.connector = None
        self.reinit()

    def reinit(self):
        self.connector = AHConnector()

    def resolve(self, barcode: str):
        self.reinit()  # prevent timeouts

        info = self.connector.get_product_by_barcode(barcode)
        print("[OK] AH API returned:", info)
        name = info.get('title')
        sub_category = info.get('subCategory')  # seems to be product type/name (without brand etc)
        print(f"[->] name={name}, sub_category={sub_category}")

        return self.RESULT_TYPES.PRODUCT.name, name, info
