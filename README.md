# barcode-shopping-list
A shopping list that can be operated with a barcode scanner


## Run API
TODO: create docker-compose.yml

    docker build -t barcodeapi src/api && docker run -it --rm -v $PWD/src/api:/app -p5000:5000 -v $PWD/lists/:/app/lists barcodeapi


## Run CLI
TODO: test within docker from remote host

    python3 src/cli/barcode_cli.py

