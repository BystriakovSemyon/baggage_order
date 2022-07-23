from marshmallow import Schema, fields
from marshmallow import validate


class BaggageSchema(Schema):
    passengerId = fields.String(
        required=True,
        validate=[validate.Length(equal=16), validate.Regexp('[a-zA-Z0-9]')],
        metadata={'description': 'Id пассажира(6ти значная строка из цифр и латинских букв)'}
    )
    routeId = fields.String(
        required=True,
        metadata={'description': 'Id маршрута(6ти значная строка из цифр и латинских букв)'}
    )
    baggageIds = fields.List(
        fields.String(validate=[validate.Length(equal=16), validate.Regexp('[a-zA-Z0-9]')]),
        required=True,
        data_key='baggageIds',
        validate=validate.Length(min=1),
        metadata={'description': 'Id багажа(6ти значная строка из цифр и латинских букв)'}
    )
    redemption = fields.Boolean(
        required=True,
        metadata={'description': 'Выкуплен(true или false)'}
    )


class BagsSchema(Schema):
    baggageSelections = fields.List(
        fields.Nested(lambda: BaggageSchema),
        required=True,
        data_key='baggageSelections',
        validate=validate.Length(min=1),
        metadata={'description': ''}
    )