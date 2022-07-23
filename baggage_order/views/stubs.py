import logging

from flask.views import MethodView
from flask_smorest import Blueprint

from baggage_order.schemas.bags import BagsSchema
from baggage_order.schemas.orders import OrdersRequestSchema, OrdersResponseSchema
from baggage_order.views.stubs_mock.orders import orders_response

stubs_blp = Blueprint('stubs', 'stubs', url_prefix='/v1/stubs', description='Заглушки для внешних систем')

logger = logging.getLogger(__name__)


@stubs_blp.route("/orders")
class Order(MethodView):
    @stubs_blp.arguments(OrdersRequestSchema, location="query")
    @stubs_blp.response(200, OrdersResponseSchema)
    def get(self, args):
        return orders_response


@stubs_blp.route("/bags")
class Bags(MethodView):
    @stubs_blp.arguments(BagsSchema)
    # @stubs_blp.response(200, OrdersSchema(many=True))
    def put(self, args):
        return "SUCCESS", 200
