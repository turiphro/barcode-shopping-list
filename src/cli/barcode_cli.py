#!/usr/bin/env python3
import json
import click
import requests
from slugify import slugify
from enum import Enum


def api_url(hostname, port, path):
    return f"http://{hostname}:{port}/api/{path}"


def padding(s: str, width: int, char=' '):
    if len(s) > width:
        return s[:width]
    else:
        return s + char * (width - len(s))


COMMANDS = Enum("COMMANDS", "ADD REMOVE LIST")

@click.command()
@click.option('--hostname', default='localhost', help='Hostname of the API')
@click.option('--port', default=7000, help='Port of the API')
@click.option('--listname', default='groc', help='List identifier')
@click.option('--width', default=30, help='Screen width (for the list width)')
def barcode_cli(hostname, port, listname, width):
    while True:
        # Show current list
        response = requests.get(api_url(hostname, port, f"lists/{listname}"))
        list = response.json()

        click.echo()
        click.echo(click.style(padding(f"=======[[ {listname} ]]===", width, "="), fg="white"))
        for item in list.get("list"):
            name = item.get("name")
            qty = item.get("quantity")
            click.echo(
                click.style(f"{qty}x", fg="white") + " " +
                click.style(padding(name, width - 3), fg="yellow")
            )
        click.echo(click.style(padding("=", width, "="), fg="white"))
        click.echo()

        command, payload = process_command_input(hostname, port)

        if command == COMMANDS.LIST.name:
            listname = payload

        else:
            #print("SENDING", command, payload)
            execute_action(command, payload, hostname, port, listname)


def process_command_input(hostname, port):
    completed = False
    command = COMMANDS.ADD.name
    payload = None

    while not completed:
        barcode_type, barcode_item = get_next_barcode(command, hostname, port)

        # Process barcode
        if barcode_type == "COMMAND":
            command = barcode_item["name"]

            if command == COMMANDS.LIST.name:
                payload = get_next_input(command)
                completed = True

        elif barcode_type == "PRODUCT":
            payload = barcode_item
            completed = True

    return command, payload


def get_next_input(command):
    return click.prompt(click.style(f"[{command}]", fg="blue"))


def get_next_barcode(command, hostname, port):
    barcode = get_next_input(command)
    response = requests.get(api_url(hostname, port, f"lookup/{barcode}"))
    payload = response.json()

    if response.status_code == 404:
        click.echo(click.style("NOT FOUND: " + payload.get("error"), fg="red"))
        return None, None
    elif response.status_code >= 300:
        click.echo(click.style("SERVER ERROR: " + payload.get("error"), fg="red"))
        return None, None

    barcode_type = payload.get('type', 'ERROR')
    barcode_item = {
        "name": payload.get('name'),
        "description": payload.get('description'),
        "barcode": payload.get('barcode'),
        "info": payload.get('info')
    }
    click.echo(click.style(barcode_type, fg="green") + ": " + click.style(barcode_item["name"], fg="yellow", bold=True))

    return barcode_type, barcode_item


def execute_action(command, payload, hostname, port, listname):
    if command == COMMANDS.ADD.name:
        requests.post(api_url(hostname, port, f"lists/{listname}"), json=payload)
    elif command == COMMANDS.REMOVE.name:
        item_id = slugify(payload.get('name') + " " + payload.get('description', ''))
        requests.delete(api_url(hostname, port, f"lists/{listname}/{item_id}"))
    elif command == COMMANDS.LIST.name:
        pass # nothing to do; refreshes next time
    else:
        print("unknown command:", command)


if __name__ == "__main__":
    barcode_cli()
