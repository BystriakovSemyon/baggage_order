import requests

from baggage_order import settings


class TestRegression:
    def test_order_skis(self, run_baggage_order):
        params = {
            'second_name': 'ivanov',
            'order_id': 'AAAAAA'
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f'http://{settings.WEB_SERVER_HOST}:{settings.WEB_SERVER_PORT}/v1/order_skis',
            params=params,
            headers=headers
        ).json()
        assert response == {"shoppingCart": {'status': 'updated'}}

    def test_order_not_found(self, run_baggage_order):
        params = {
            'second_name': 'fail',
            'order_id': 'AAAAAA'
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f'http://{settings.WEB_SERVER_HOST}:{settings.WEB_SERVER_PORT}/v1/order_skis',
            params=params,
            headers=headers
        )
        assert response.status_code == 404

    def test_order_unprocessable_entity(self, run_baggage_order):
        params = {
            'second_name': 'fail',
            'order_id': 'fail'
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f'http://{settings.WEB_SERVER_HOST}:{settings.WEB_SERVER_PORT}/v1/order_skis',
            params=params,
            headers=headers
        )
        assert response.status_code == 422
