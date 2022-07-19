import os

import flask
from flask_smorest import Api

from baggage_order import settings
from baggage_order.views.orders import orders_blp

app = flask.Flask(settings.APP_NAME)
app.config.update(settings.FLASK_CONFIG)
api = Api(app)
api.register_blueprint(orders_blp)

def swagger_send_static_file(filename):
    """Отдает файлы для swagger-ui"""
    swagger_static = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../swagger-ui')
    if not os.path.isdir(swagger_static):
        flask.abort(500)

    cache_timeout =app.get_send_file_max_age(filename)
    return flask.send_from_directory(
        swagger_static, filename, cache_timeout=cache_timeout
    )

# В README требованиях сервиса описано это ограничение
app.add_url_rule(
    settings.FLASK_CONFIG['OPENAPI_SWAGGER_UI_URL'] + '<path:filename>',
    endpoint='swagger-static',
    host=None,
    view_func=swagger_send_static_file,
)
