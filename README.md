# barcode-shopping-list
A shopping list that can be operated with a barcode scanner


## Run API + WEB

Run:

    docker-compose up

The API runs on port 7000, the static website on port 7001.

Or run with docker directly:

    docker build -t barcodeapi src/api && docker run -it --rm -v $PWD/src/api:/app -p7000:5000 -v $PWD/lists/:/app/lists barcodeapi

    docker run -it --rm -v $PWD/src/web/static:/web -p7001:8080 halverneus/static-file-server


## Run CLI
TODO: test within docker from remote host

    python3 src/cli/barcode_cli.py

Instructions for a raspberry pi with LCD screen:

    # 1. Install Raspberry Pi OS Lite (without GUI)
    # 2. Configure wifi:
    #    https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
    # 3. sudo apt update && sudo apt install git python3-pip
    # 3. Checkout this repo in $HOME;
    #    might want to `ssh-keygen` and add the key to github first;
    #    git clone ssh://git@github.com/turiphro/barcode-shopping-list
    # 4. Configure LCD screen:
    #    ./install_rpi.sh

