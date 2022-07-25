import logging

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from baggage_order.schemas.bags import BagsSchema, BagsResponseSchema
from baggage_order.schemas.orders import OrdersRequestSchema, OrdersResponseSchema
from baggage_order.views.stubs_mock.orders import orders_response
from baggage_order.views.stubs_mock.register_service import bags_response

stubs_blp = Blueprint('stubs', 'stubs', url_prefix='/v1/stubs', description='Заглушки для внешних систем')

logger = logging.getLogger(__name__)


@stubs_blp.route("/orders")
class Order(MethodView):
    @stubs_blp.arguments(OrdersRequestSchema(), location="query")
    @stubs_blp.response(200, OrdersResponseSchema())
    def get(self, orders_request_json: dict) -> dict:
        if orders_request_json['number'] == 'AAAAAA' and orders_request_json['passengerId'] == 'ivanov':
            return orders_response
        else:
            abort(404, message="Order not found")


@stubs_blp.route("/bags")
class Bags(MethodView):
    @stubs_blp.arguments(BagsSchema())
    @stubs_blp.response(200, BagsResponseSchema())
    def put(self, args: dict) -> dict:
        return bags_response
