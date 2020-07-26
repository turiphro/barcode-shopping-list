import logging
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException


logger = logging.getLogger(__name__)

STATIC_DATA = {1: ['kattenzand', 'brokjes', 'snoepjes']}


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

    return api