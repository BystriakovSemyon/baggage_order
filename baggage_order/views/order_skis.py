import logging

import flask
import requests
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from baggage_order import settings
from baggage_order.schemas.bags import BagsSchema, BagsResponseSchema
from baggage_order.schemas.order_skis import OrderSkiSchema
from baggage_order.schemas.orders import OrdersResponseSchema, OrdersRequestSchema

order_skis_blp = Blueprint('order_skis', 'order_skis', url_prefix='/v1/order_skis', description='Бронирование лыж')

logger = logging.getLogger(__name__)


@order_skis_blp.route("/")
class Order(MethodView):
    @order_skis_blp.arguments(OrderSkiSchema(), location="query")
    @order_skis_blp.response(200, BagsResponseSchema())
    def get(self, order_ski_query: dict) -> dict:
        if order_ski_query['order_id'] == 'AAAAAA' and order_ski_query['second_name'] == 'ivanov':
            orders_list = self.get_orders(order_ski_query=order_ski_query)
            orders_list_parsed = OrdersResponseSchema().loads(orders_list)
            return self.put_bags(orders_list=orders_list_parsed)
        else:
            abort(404, message="Order not found")

    def validate_orders_query(self, params: dict) -> None:
        validate = OrdersRequestSchema().dumps(params)
        OrdersRequestSchema().loads(validate)

    def get_orders(self, order_ski_query: dict) -> str:
        """GET request to integration to receive all orders."""
        params = {
            'passengerId': order_ski_query['second_name'],
            'number': order_ski_query['order_id']
        }
        self.validate_orders_query(params)
        return requests.get(
            f"http://{settings.APP_NAME}:{settings.WEB_SERVER_PORT}{flask.url_for('stubs.Order')}",
            params=params
        ).text

    def construct_bags_query(self, orders_list: dict) -> list:
        """
        Constructs PUT data for /bags request.

        If there is no baggage order for any person/flight, we think that we can't serve this request.
        If there are several baggage skis orders per flight, we set random one
        because it is fixed in the web service requirements.
        """
        baggage_selections = []
        for ancillarie_pricing in orders_list['ancillariesPricings']:
            for baggage_pricing in ancillarie_pricing['baggagePricings']:
                baggage_ids = []
                for baggage in baggage_pricing['baggages']:
                    if baggage.get('equipmentType') == 'ski':
                        baggage_ids.append(baggage['id'])
                for passanger_id in baggage_pricing['passengerIds']:
                    baggage_selections.append({
                     "passengerId": passanger_id,
                     "routeId": baggage_pricing['routeId'],
                     "baggageIds": baggage_ids,
                     "redemption": False
                  })
        return baggage_selections

    def put_bags(self, orders_list: dict) -> dict:
        """PUT request to integration to register baggage(ski)."""
        baggage_selections = self.construct_bags_query(orders_list)
        query = {'baggageSelections': baggage_selections}
        data = BagsSchema().dumps(query)
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        return requests.put(
            f"http://{settings.APP_NAME}:{settings.WEB_SERVER_PORT}{flask.url_for('stubs.Bags')}",
            headers=headers,
            data=data
        ).json()
