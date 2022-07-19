import logging
import logging.config
from waitress import serve
from web_server import app

from baggage_order import settings


def setup_logger():
    logging.config.dictConfig(settings.LOGGING)


if __name__ == '__main__':
    setup_logger()
    print('Start flask (waitress)!')
    serve(app, host=settings.WEB_SERVER_HOST, port=settings.WEB_SERVER_PORT)


