import pytest
from waitress import serve
import multiprocessing

from time import sleep

from baggage_order import settings
from baggage_order.web_server import app


@pytest.fixture
def run_baggage_order():
    process = multiprocessing.Process(
        target=serve,
        args =(app,),
        kwargs={'host': settings.WEB_SERVER_HOST, 'port': settings.WEB_SERVER_PORT}
    )
    process.daemon = True
    process.start()
    # We need to check server health here
    sleep(1)
    yield process
    process.join(timeout=1.0)
