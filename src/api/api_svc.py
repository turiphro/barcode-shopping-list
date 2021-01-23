import logging
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

from resolvers.albert_heijn import AlbertHeijnResolver
from resolvers.commands import CommandResolver

logger = logging.getLogger(__name__)

STATIC_DATA = {1: ['kattenzand', 'brokjes', 'snoepjes']}
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
        list_data = STATIC_DATA.get(int(list_id), [])
        return jsonify(list=list_data)

    @api.route('/api/lookup/<barcode>', methods=['GET'])
    def lookup_barcode(barcode):
        result_type = name = info = None
        for resolver in RESOLVERS:
            try:
                result_type, name, info = resolver.resolve(barcode)
                break
            except Exception as e:
                print("! cannot resolve barcode {}: {}".format(barcode, e))
                print(e)
                # TODO throw 404 or 500
        # TODO: failed, so show 404
        return jsonify(
            type=result_type,
            name=name,
            info=info
        )

    return api
