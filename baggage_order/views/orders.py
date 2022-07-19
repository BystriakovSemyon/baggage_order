from flask_smorest import Blueprint


orders_blp = Blueprint('orders', 'orders', url_prefix='/v1/orders', description='Hello, World!')


@orders_blp.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
