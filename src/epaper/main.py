import network
import urequests
import ujson
import time

from pico_epaper import EPD_2in9_Landscape


# in micropython, open env.json and read the values
ENV = ujson.loads(open("env.json").read())
SSID = ENV["ssid"]
PASSWORD = ENV["password"]
LIST_NAME = ENV["list_name"]

API_BASE = "http://groc.turiphro.nl/api/"


class Internet():
    def __init__(self, ssid, password):
        self.wlan = network.WLAN(network.STA_IF)
        self.__ssid = ssid
        self.__password = password

    def connect(self):
        #Connect to WLAN
        self.wlan.active(True)
        self.wlan.connect(self.__ssid, self.__password)
        while self.wlan.isconnected() == False:
            print('Waiting for connection...')
            time.sleep(1)
        ip = self.wlan.ifconfig()[0]
        print(f'Connected on {ip}')

    def reconnect_if_needed(self):
        if not self.wlan.isconnected():
            print("Reconnecting wifi..")
            self.wlan.disconnect()
            self.wlan.active(False)
            self.connect()


def fetch_groceries_list(list_name: str):
    url = f"{API_BASE}lists/{list_name}"
    print(f"Requesting current groceries list from {url}")

    response = urequests.get(url, timeout=10)

    groc_list = response.json().get("list", [])
    return groc_list


def display_list(items: dict):
    # Landscape
    epd = EPD_2in9_Landscape()
    epd.Clear(0xff)
    epd.fill(0xff)

    for i, item in enumerate(items):
        line = f"{item['quantity']}x {item['name']}"

        y = 5 + 10 * i
        epd.text(line, 0, y, 0x00)

    epd.display(epd.buffer)
    epd.delay_ms(2000)


def display_error(error: str, line_count=5):
    # overlay
    epd = EPD_2in9_Landscape()

    epd.rect(18, 18, 254, line_count * 10 + 4, 0xff, True)
    epd.rect(18, 18, 254, line_count * 10 + 34, 0x00, False)
    lines = error.split("\n")
    for i in range(min(line_count, len(lines))):
        epd.text(lines[i], 20, 20 + i * 10, 0x00)

    epd.display(epd.buffer)
    epd.delay_ms(2000)


if __name__ == "__main__":
    from machine import Pin
    led = Pin("LED", Pin.OUT)
    led.on()

    # one time connecting and loading the list
    internet = Internet(SSID, PASSWORD)
    internet.connect()

    # refresh screen with latest
    last_items = []
    while True:
        try:
            groc_list = fetch_groceries_list(LIST_NAME)
            items = [{key: item[key] for key in ["name", "description", "quantity"]} for item in groc_list]
            print(f"Current list: {items}")
            
            if items != last_items:
                last_items = items
                display_list(items)

        except Exception as ex:
            print(f"EXCEPTION: {ex.__class__.__name__}: {ex}")
            display_error(f"{ex.__class__.__name__}\n{ex}")

            print(f"Trying to reconnect")
            internet.reconnect_if_needed()

        time.sleep(5)

