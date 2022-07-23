from marshmallow import Schema, fields
from marshmallow import validate


class OrderSkiSchema(Schema):
    order_id = fields.String(
        required=True,
        validate=[validate.Length(equal=6), validate.Regexp('[a-zA-Z0-9]')],
        metadata={'description': 'Номер заказа(6ти значная строка из цифр и латинских букв)'}
    )
    second_name = fields.String(
        required=True,
        validate=[validate.Length(min=1, max=255), validate.Regexp('[a-zA-Z]')],
        metadata={'description': 'Фамилия латиницей'}
    )
