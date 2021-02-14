import logging
import traceback
from flask import Flask, request, jsonify, abort
from werkzeug.exceptions import HTTPException
import dataclasses

from resolvers.albert_heijn import AlbertHeijnResolver
from resolvers.commands import CommandResolver
from models.item import Item
from storage.storage import Storage
from storage.csv_file import CsvFile


logger = logging.getLogger(__name__)

CSV_STORAGE = "/app/lists"
RESOLVERS = [AlbertHeijnResolver(), CommandResolver()]


def create_api():
    api = Flask(__name__)
    api.config["DEBUG"] = True

    storage: Storage = CsvFile(CSV_STORAGE)

    @api.errorhandler(Exception)
    def make_json_error(ex: Exception):
        logger.error(ex)
        response = jsonify(error=str(ex))
        response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
        return response

    @api.route('/', methods=['GET'])
    def hello():
        return jsonify(message='Hi!')

    @api.route('/api/lists/<list_id>', methods=['GET'])
    def index(list_id):
        list_data = storage.get(list_id)
        return jsonify(list=list(map(dataclasses.asdict, list_data)))

    @api.route('/api/lists/<list_id>', methods=['POST'])
    def add_item(list_id):
        """Adding item to list. Expected fields: name, description (opt), info (opt, dict), quantity (opt, int)"""
        data = request.json
        new_item = Item(**data)
        storage.add_item(list_id, new_item)
        list_data = storage.get(list_id)
        return jsonify(list=list(map(dataclasses.asdict, list_data)))

    @api.route('/api/lists/<list_id>/<item_name>', methods=['DELETE'])
    def remove_item(list_id, item_name):
        storage.remove_item(list_id, item_name)
        list_data = storage.get(list_id)
        return jsonify(list=list(map(dataclasses.asdict, list_data)))

    @api.route('/api/lookup/<barcode>', methods=['GET'])
    def lookup_barcode(barcode):
        for resolver in RESOLVERS:
            try:
                result_type, item = resolver.resolve(barcode)

                return jsonify(
                    type=result_type,
                    name=item.name,
                    description=item.description,
                    info=item.info
                )
            except Exception as e:
                print("! cannot resolve barcode {}: {}".format(barcode, e))
                traceback.print_exc()
                # TODO throw 404 or 500
        # failed, so show 404
        abort(404, "Barcode couldn't be resolved.")

    return api
