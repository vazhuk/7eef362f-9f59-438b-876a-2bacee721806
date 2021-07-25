import json
import random

from app import app
from flask import request
from werkzeug import exceptions


@app.route('/ping')
def ping():
    return "pong"


@app.route('/generate', methods=['POST'])
def generate():
    args = request.args
    if 'model_name' in args:
        model_name = args.get('model_name')
        return {'model_name': model_name, 'result': random.randint(0, 10_000)}
    else:
        raise exceptions.BadRequest(f'Can`t find `model_name` parameter in: {list(args)}')


@app.errorhandler(exceptions.HTTPException)
def handle_exceptions(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response, e.code
