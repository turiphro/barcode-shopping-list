import logging
from flask import Flask, request, jsonify, abort
from werkzeug.exceptions import HTTPException

from resolvers.albert_heijn import AlbertHeijnResolver
from resolvers.commands import CommandResolver

logger = logging.getLogger(__name__)

STATIC_DATA = {
    'groc': ['kattenzand', 'brokjes', 'snoepjes']
}
RESOLVERS = [AlbertHeijnResolver(), CommandResolver()]


def create_api():
    api = Flask(__name__)
    api.config["DEBUG"] = True


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
        list_data = STATIC_DATA.get(list_id, [])
        return jsonify(list=list_data)

    @api.route('/api/lists/<list_id>', methods=['POST'])
    def add_item(list_id):
        new_item = request.json
        STATIC_DATA.get(list_id, []).append(new_item.get("name"))
        list_data = STATIC_DATA.get(list_id, [])
        return jsonify(list=list_data)

    @api.route('/api/lists/<list_id>/<item_name>', methods=['DELETE'])
    def remove_item(list_id, item_name):
        list_data = STATIC_DATA.get(list_id, [])
        if item_name in list_data:
            list_data.remove(item_name)
        list_data = STATIC_DATA.get(list_id, [])
        return jsonify(list=list_data)

    @api.route('/api/lookup/<barcode>', methods=['GET'])
    def lookup_barcode(barcode):
        for resolver in RESOLVERS:
            try:
                result_type, name, info = resolver.resolve(barcode)

                return jsonify(
                    type=result_type,
                    name=name,
                    info=info
                )
            except Exception as e:
                print("! cannot resolve barcode {}: {}".format(barcode, e))
                print(e)
                # TODO throw 404 or 500
        # failed, so show 404
        abort(404, "Barcode couldn't be resolved.")

    return api
