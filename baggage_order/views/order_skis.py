import logging

import flask
import requests
from flask.views import MethodView
from flask_smorest import Blueprint

from baggage_order.schemas.order_skis import OrderSkiSchema
from baggage_order.schemas.orders import OrdersResponseSchema

order_skis_blp = Blueprint('order_skis', 'order_skis', url_prefix='/v1/order_skis', description='Бронирование лыж')

logger = logging.getLogger(__name__)


@order_skis_blp.route("/")
class Order(MethodView):
    @order_skis_blp.arguments(OrderSkiSchema, location="query")
    # @stubs_blp.response(200, OrdersSchema(many=True))
    def get(self, order_ski_query: dict):
        orders_list = self.get_orders(order_ski_query=order_ski_query)
        orders_list_parsed = OrdersResponseSchema().loads(orders_list)
        self.put_bags(orders_list=orders_list_parsed)
        return "SUCCESS", 200

    def get_orders(self, order_ski_query: dict) -> dict:
        """GET request to integration to receive all orders."""
        params = {
            'passengerId': order_ski_query['second_name'],
            'number': order_ski_query['order_id']
        }
        return requests.get(f"http://baggage_order:8080{flask.url_for('stubs.Order')}", params=params).json()

    def put_bags(self, orders_list):
        """PUT request to integration to register baggage(ski)."""
        pass

    request = {
       "baggageSelections":[
          {
             "passengerId":"dKCLeweYNb6iDO66",
             "routeId":"RyucZ4TVI1EseYCp",
             "baggageIds":[
                "siEct88JoxGWpe5v"
             ],
             "redemption": False
          },
          {
             "passengerId":"dKCLeweYNb6iDO66",
             "routeId":"iqCrFYw8oDTwVpWD",
             "baggageIds":[
                "CMQs0BgMVGpAJcOP"
             ],
             "redemption": False
          },
          {
             "passengerId":"qauJTpuMlDrASaty",
             "routeId":"RyucZ4TVI1EseYCp",
             "baggageIds":[
                "siEct88JoxGWpe5v"
             ],
             "redemption": False
          },
          {
             "passengerId":"qauJTpuMlDrASaty",
             "routeId":"iqCrFYw8oDTwVpWD",
             "baggageIds":[
                "CMQs0BgMVGpAJcOP"
             ],
             "redemption": False
          }
       ]
    }
