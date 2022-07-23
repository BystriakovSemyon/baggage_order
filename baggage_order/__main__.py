
import logging.config

from waitress import serve

from baggage_order import settings

if __name__ == '__main__':
    # Init logging at first to start send logs to logstash
    logging.config.dictConfig(settings.LOGGING)
    logger = logging.getLogger(__name__)

    from baggage_order.web_server import app
    logger.info('Start flask (waitress)!')
    serve(app, host=settings.WEB_SERVER_HOST, port=settings.WEB_SERVER_PORT)
