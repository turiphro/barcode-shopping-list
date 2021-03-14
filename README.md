# barcode-shopping-list
A shopping list that can be operated with a barcode scanner.


## Design
Here's a professional design diagram:

    +------------------------+                                     +-------------------------+
    | Command line interface | ----------------------------------> | REST API                |
    |  (Raspberry Pi + LCD)  |                           --------> | (Python + CSV + Docker) |
    +------------------------+                          /          +-------------------------|
                ^                                      /
                |               +---------------------------+
             barcode            | Web interface             |
             scanner            | (static React page)       |
                                +---------------------------+

## Demo

[![Youtube preview](https://img.youtube.com/vi/31pYClpleRU/0.jpg)](https://www.youtube.com/watch?v=31pYClpleRU)

## Run API + WEB

The API and website can be run on any server. If you want to use the web interface outside of
your home (e.g., in the super market), it'll need to be publicly accessible. There's an
example config for Nginx in `etc/`. Data is saved in CSV files (hey, it's a hack) which are
mount to the host OS.

The barcode lookup API currently supports Albert Heijn and Jumbo products, and plaintext input.

Run:

    docker-compose up

The API runs on port 7000, the static website on port 7001.

Or run with docker directly:

    docker build -t barcodeapi src/api && docker run -it --rm -v $PWD/src/api:/app -p7000:5000 -v $PWD/lists/:/app/lists barcodeapi

    docker run -it --rm -v $PWD/src/web/static:/web -p7001:8080 halverneus/static-file-server


## Run CLI

Run:

    python3 src/cli/barcode_cli.py [--hostname your.url.com --port 80]

    OR:

    docker build -t barcodecli src/cli
    docker run -it --rm -v $PWD/src/cli:/app barcodecli [--hostname your.url.com --port 80]

Instructions for installing a raspberry pi with LCD screen:

1. Install Raspberry Pi OS Lite (without GUI)
2. Configure wifi:
   https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
3. sudo apt update && sudo apt install git python3-pip
3. Checkout this repo in $HOME;
   might want to `ssh-keygen` and add the key to github first;
   git clone ssh://git@github.com/turiphro/barcode-shopping-list
4. Configure LCD screen:
   `./install_rpi.sh`
5. Configure autostart; add the run command from above to your `.profile` or `rc.local` file.

