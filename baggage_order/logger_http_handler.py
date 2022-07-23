import json
import logging
import os
import socket
import threading
from logging.handlers import HTTPHandler

import requests
from urllib3.util import Timeout

from baggage_order import settings


class LogstashHandler(HTTPHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.http_session = requests.Session()
        self.send_lock = threading.RLock()

    def create_payload(self, record: logging.LogRecord):
        log_rec_map = {
            'app_name': settings.APP_NAME,
            'hostname': socket.gethostname(),
            'name': record.name,
            'funcName': record.funcName,
            'levelname': record.levelname,
            'message': record.getMessage(),
            'exc_text': str(record.exc_text) if record.exc_text else None,
            'process_name': record.processName,
            'thread_name': record.threadName,
            'uptime': int(record.relativeCreated / 1000),
        }
        if hasattr(record, 'extra'):
            log_rec_map.update(record.extra)
        payload = json.dumps(log_rec_map).encode('utf-8')
        return payload

    def emit(self, record):
        timeout = Timeout(settings.LOGSTASH_LOGGER_HANDLER_TIMEOUT, settings.LOGSTASH_LOGGER_HANDLER_TIMEOUT)
        with self.send_lock:
            try:
                self.http_session.post(
                    settings.LOGSTASH_HOST,
                    timeout=timeout,
                    data=self.create_payload(record),
                    headers={'Content-type': 'application/json'}
                )
            except Exception:
                logging.getLogger('console').error('LogstashHandler is failed!', exc_info=True)
                if logging.raiseExceptions:
                    os._exit(1)
