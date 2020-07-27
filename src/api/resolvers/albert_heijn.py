from supermarktconnector.ah import AHConnector


class AlbertHeijnResolver:
    def __init__(self):
        self.connector = AHConnector()

    def resolve(self, barcode):
        info = self.connector.get_product_by_barcode(barcode)
        title = info.get('title')

        return (title, info)
