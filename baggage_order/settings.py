import os
import sys

APP_NAME = os.getenv('APP_NAME', 'baggage_order')
WEB_SERVER_HOST = os.getenv('WEB_SERVER_HOST', '0.0.0.0')
WEB_SERVER_PORT = os.getenv('WEB_SERVER_PORT', '80')

REST_SWAGGER_UI_ENABLED = os.getenv('REST_SWAGGER_UI_ENABLED', True)
SWAGGER_STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../swagger-ui')

FLASK_CONFIG = {
    'API_TITLE': os.getenv('API_TITLE', 'Baggage order'),
    'API_VERSION': os.getenv('API_VERSION', 'v1'),
    'OPENAPI_VERSION': os.getenv('OPENAPI_VERSION', '3.0.2')
}

if REST_SWAGGER_UI_ENABLED:
    FLASK_CONFIG['OPENAPI_JSON_PATH'] = os.getenv('OPENAPI_JSON_PATH', '/api-spec.json')
    FLASK_CONFIG['OPENAPI_URL_PREFIX'] = os.getenv('OPENAPI_URL_PREFIX', '/')
    FLASK_CONFIG['OPENAPI_SWAGGER_UI_PATH'] = os.getenv('OPENAPI_SWAGGER_UI_PATH', '/swagger-ui')
    FLASK_CONFIG['OPENAPI_SWAGGER_UI_URL'] = os.getenv('OPENAPI_SWAGGER_UI_URL', '/swagger-ui/')

LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', 'http://logstash:4441')
LOGSTASH_LOGGER_HANDLER_TIMEOUT = int(os.getenv('LOGSTASH_LOGGER_HANDLER_TIMEOUT', 10))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
        'http': {
            'class': 'baggage_order.logger_http_handler.LogstashHandler',
            'url': '',
            'host': '',
            'level': 'INFO'
        }
    },
    'loggers': {
        'console': {'handlers': ['console'], 'level': 'INFO', 'propagate': False}
    },
    'root': {
        'handlers': ['console', 'http'],
        'level': 'INFO'
    }
}
