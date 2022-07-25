import logging
import os
import traceback
from time import strftime

import flask
from flask import request
from flask_smorest import Api

from baggage_order import settings
from baggage_order.views.order_skis import order_skis_blp
from baggage_order.views.stubs import stubs_blp

app = flask.Flask(settings.APP_NAME)
app.config.update(settings.FLASK_CONFIG)
api = Api(app)
api.register_blueprint(order_skis_blp)
api.register_blueprint(stubs_blp)

logger = logging.getLogger(__name__)


@app.after_request
def after_request(response: flask.Response) -> flask.Response:
    """Log all requests-response"""
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    response.direct_passthrough = False
    logger.info(
        f'{timestamp}, {request.remote_addr}, {request.method}, {request.scheme}, {request.full_path}, {response.status}',
        extra={'extra': {
            'response_text': response.get_data(as_text=True),
            'request_text': request.get_data(as_text=True)
        }}
    )
    return response


@app.errorhandler(Exception)
def exceptions(e) -> int:
    """Log all exceptions"""
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.exception(
        f'{timestamp}, {request.remote_addr}, {request.method}, {request.scheme}, {request.full_path}, {traceback.format_exc()}',
        extra={'extra': {'request_text': request.get_data(as_text=True)}}
    )
    return e.status_code


def swagger_send_static_file(filename: str):
    """Отдает файлы для swagger-ui"""
    swagger_static = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../swagger-ui')
    if not os.path.isdir(swagger_static):
        flask.abort(500)

    cache_timeout = app.get_send_file_max_age(filename)
    return flask.send_from_directory(
        swagger_static, filename, cache_timeout=cache_timeout
    )

app.add_url_rule(
    settings.FLASK_CONFIG['OPENAPI_SWAGGER_UI_URL'] + '<path:filename>',
    endpoint='swagger-static',
    host=None,
    view_func=swagger_send_static_file,
)
