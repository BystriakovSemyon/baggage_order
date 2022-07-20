import logging
from flask_smorest import Blueprint


order_skis_blp = Blueprint('order_skis', 'order_skis', url_prefix='/v1/order_skis', description='Order skis')

logger = logging.getLogger(__name__)


@order_skis_blp.route("/")
def create_skis_order():
    logger.info('Run create_skis_order')
    return "<p>Skis are ordered!</p>"
