import logging
import flask
from flask import  request, jsonify
from werkzeug.exceptions import HTTPException


logger = logging.getLogger(__name__)

STATIC_DATA = {1: ['kattenzand', 'brokjes', 'snoepjes']}

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.errorhandler(Exception)
def make_json_error(ex: Exception):
    logger.error(ex)
    response = jsonify(error=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response

@app.route('/', methods=['GET'])
def hello():
    return jsonify(message='Hi!')

@app.route('/api/lists/<list_id>', methods=['GET'])
def index(list_id):
    list_data = STATIC_DATA.get(int(list_id), [])
    return jsonify(list=list_data)

app.run()
