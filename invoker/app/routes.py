import json

from app import app
from flask import request
from werkzeug import exceptions

from config.config import *
from cache.cache import Cache
from service.prediction_fetcher import PredictionFetcher

cache = Cache(redis_host=REDIS_HOST, redis_port=REDIS_PORT)
prediction_service = PredictionFetcher(generator_host=GENERATOR_HOST,
                                       generator_port=GENERATOR_PORT,
                                       models=MODEL_NAMES)


def run_cascade(viewer_id):
    result = prediction_service.fetch_predictions(viewer_id)
    return {'viewerid': viewer_id, 'recommendations': result}


@app.route('/ping')
def ping():
    return "pong"


@app.route('/recommend', methods=['GET'])
def recommend():
    args = request.args
    if 'viewerid' in args:
        viewer_id = args['viewerid']
        cached_value = cache.get_key(viewer_id)
        if not cached_value:
            recommendations = run_cascade(viewer_id)
            cache.cache(viewer_id, recommendations)
            return recommendations
        else:
            return cached_value
    else:
        raise exceptions.BadRequest(f'Can`t find `viewerid` parameter in: {list(args)}')


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
