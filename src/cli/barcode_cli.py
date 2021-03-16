#!/usr/bin/env python3
import click
import requests
import os
import sys
from slugify import slugify
from enum import Enum
from typing import List, Dict, Tuple


COMMANDS = Enum("COMMANDS", "ADD REMOVE LIST REFRESH EXIT SHUTDOWN UPDATE")

@click.command()
@click.option('--hostname', default='localhost', help='Hostname of the API')
@click.option('--port', default=7000, help='Port of the API')
@click.option('--listname', default='groc', help='List identifier')
@click.option('--width', default=40, help='Screen width (for the list width)')
def barcode_cli(hostname, port, listname, width):
    while True:
        # Fetch and show current list
        response = requests.get(api_url(hostname, port, f"lists/{listname}"))
        if response.status_code != 200:
            click.echo(click.style(f"Invalid API response (code {response.status_code}):"\
                                   f"\n{response.content[:200]}..", fg="red"))
        else:
            items = response.json()
            print_list(listname, items, width)

        # Process command line input
        handler = InputHandler(hostname, port)
        while not handler.finished:
            handler.handle_next()

        command, item = handler.get()

        # Execute parsing result
        if command == COMMANDS.LIST.name:
            listname = item.get("name")
        elif command == COMMANDS.REFRESH.name:
            pass  # simply refresh in next iteration
        else:
            execute_action(command, item, hostname, port, listname)


class InputHandler:
    def __init__(self, hostname, port):
        # config
        self.hostname = hostname
        self.port = port

        # processing vars
        self.finished = False
        self.quantity = 1

        # outputs
        self.command = COMMANDS.ADD.name
        self.item = None

    def handle_next(self):
        barcode = click.prompt(
            click.style(f"[{self.command}]", fg="blue") +
            click.style(f"[{self.quantity}x]" if self.quantity > 1 else "", fg="cyan")
        )

        response = requests.get(api_url(self.hostname, self.port, f"lookup/{barcode}"))

        if response.status_code == 404:
            click.echo(click.style("NOT FOUND: " + response.json().get("error"), fg="red"))
            return
        elif response.status_code >= 300:
            click.echo(click.style(
                f"SERVER ERROR ({response.status_code}): {response.content[:200]}..", fg="red"))
            return

        payload = response.json()
        barcode_type = payload.get('type', 'ERROR')
        item = {field: payload.get(field)
                for field in ["name", "description", "barcode", "resolver", "info"]}
        click.echo(
            click.style(barcode_type, fg="green") + ": " + click.style(item["name"], fg="yellow", bold=True))

        # Process barcode
        if barcode_type == "PRODUCT":
            self.item = item
            self.finished = True

        elif barcode_type == "COMMAND":
            # Commands handled in this handler
            if item["name"] in ["1X", "2X", "3X", "4X"]:
                self.quantity = int(item["name"][:-1])
            # Commands handled in main loop
            elif item["name"] in ["EXIT", "SHUTDOWN", "UPDATE", "REFRESH"]:
                self.command = item["name"]
                self.finished = True
            # Commands requiring further parsing
            else:
                self.command = item["name"]
                self.quantity = 1

    def get(self) -> Tuple[str, Dict]:
        if self.item and self.quantity > 1:
            self.item["quantity"] = self.quantity
        return self.command, self.item


def execute_action(command, payload, hostname, port, listname):
    if command == COMMANDS.ADD.name:
        requests.post(api_url(hostname, port, f"lists/{listname}"), json=payload)
    elif command == COMMANDS.REMOVE.name:
        item_id = slugify(payload.get('name') + " " + payload.get('description', ''))
        requests.delete(api_url(hostname, port, f"lists/{listname}/{item_id}"))
    elif command in [COMMANDS.LIST.name, COMMANDS.REFRESH.name]:
        pass  # nothing to do; handled in main loop
    elif command == COMMANDS.EXIT.name:
        click.echo(click.style("Exiting.", fg="green"))
        sys.exit(0)
    elif command == COMMANDS.SHUTDOWN.name:
        click.echo(click.style("Shutting down.", fg="green"))
        os.system("shutdown -h now")
    elif command == COMMANDS.UPDATE.name:
        click.echo(click.style("Updating...", fg="green"))
        os.system("git pull --rebase")
        os.execv(sys.argv[0], sys.argv)  # restart itself
    else:
        print("unknown command:", command)


def api_url(hostname, port, path):
    return f"http://{hostname}:{port}/api/{path}"


def print_list(listname: str, list: List[Dict], width: int):
    click.echo()
    click.echo(click.style(padding(f"=============[[ {listname} ]]===", width, "="), fg="white"))
    for item in list.get("list"):
        name = item.get("name")
        description = item.get("description")
        qty = item.get("quantity")
        click.echo(
            click.style(str(qty), fg="bright_white" if qty > 1 else None) + "x " +
            click.style(name[:width], fg="yellow") +
            padding(f" - {description}" if description else "",
                    width - min(len(name), width) - 3)
        )
    click.echo(click.style(padding("=", width, "="), fg="white"))
    click.echo()


def padding(s: str, width: int, char=' '):
    if len(s) > width:
        return s[:width]
    else:
        return s + char * (width - len(s))


if __name__ == "__main__":
    barcode_cli()
