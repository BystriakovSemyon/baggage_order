from marshmallow import Schema, fields
from marshmallow import validate


class OrdersRequestSchema(Schema):
    number = fields.String(
        required=True,
        validate=[validate.Length(equal=6), validate.Regexp('[a-zA-Z0-9]')],
        metadata={'description': 'Номер брони(6ти значная строка из цифр и латинских букв)'}
    )
    passengerId = fields.String(
        required=True,
        validate=[validate.Length(min=1, max=255), validate.Regexp('[a-zA-Z]')],
        metadata={'description': 'Id пассажира(Строка из латинских символов от 1 до 255)'}
    )


class WeightSchema(Schema):
    amount = fields.Int()
    unit = fields.String(validate=[validate.Length(equal=2), validate.Regexp('[A-Z]')])


class BaggageSchema(Schema):
    id = fields.String(validate=[validate.Length(equal=16), validate.Regexp('[a-zA-Z0-9]')])
    overWeight = fields.Boolean(required=True)
    amount = fields.Int()
    unit = fields.String(validate=[validate.Length(equal=2), validate.Regexp('[a-zA-Z0-9]')])
    weight = fields.Nested(lambda: WeightSchema)
    code = fields.String(validate=[validate.Regexp('[a-zA-Z0-9]')])
    descriptions = fields.List(
        fields.String(validate=[validate.Length(max=255)]),
        required=True,
        data_key='descriptions',
        validate=validate.Length(min=1),
        metadata={'description': 'Описания'}
    )
    registered = fields.Boolean(
        required=True,
        metadata={'description': 'Зарегистрирован'}
    )
    equipmentType = fields.String()


class BaggagePricingSchema(Schema):
    passengerIds = fields.List(
        fields.String(validate=[validate.Length(equal=16), validate.Regexp('[a-zA-Z0-9]')]),
        required=True,
        data_key='passengerIds',
        validate=validate.Length(min=1),
        metadata={'description': ''}
    )
    passengerTypes = fields.List(
        fields.String(validate=[validate.Length(equal=3), validate.Regexp('[A-Z]')]),
        required=True,
        data_key='passengerTypes',
        validate=validate.Length(min=1),
        metadata={'description': ''}
    )
    purchaseType = fields.String(
        required=True,
        validate=[validate.Length(min=1, max=255), validate.Regexp('[a-zA-Z]')],
        metadata={'description': ''}
    )
    routeId = fields.String(validate=[validate.Length(equal=16), validate.Regexp('[a-zA-Z0-9]')])
    baggages = fields.List(
        fields.Nested(lambda: BaggageSchema),
        required=True,
        data_key='baggages',
        validate=validate.Length(min=1),
        metadata={'description': ''}
    )

class AncillariePriceSchema(Schema):
    airId = fields.UUID(
        required=True,
        metadata={'description': 'Номер брони(6ти значная строка из цифр и латинских букв)'}
    )
    baggagePricings = fields.List(
        fields.Nested(lambda: BaggagePricingSchema),
        required=True,
        data_key='baggagePricings',
        validate=validate.Length(min=1),
        metadata={'description': ''}
    )
    baggageDisabled = fields.Boolean(
        required=True,
        metadata={'description': 'Багаж недоступен'}
    )
    seatsDisabled = fields.Boolean(
        required=True,
        metadata={'description': 'Места недостапны'}
    )
    mealsDisabled = fields.Boolean(
        required=True,
        metadata={'description': 'Еда недоступна'}
    )
    upgradesDisabled = fields.Boolean(required=True)
    loungesDisabled = fields.Boolean(required=True)
    fastTracksDisabled = fields.Boolean(required=True)
    petsDisabled = fields.Boolean(
        required=True,
        metadata={'description': 'Перевоз животных недоступен'}
    )


class OrdersResponseSchema(Schema):
    ancillariesPricings = fields.List(
        fields.Nested(lambda: AncillariePriceSchema),
        required=True,
        data_key='ancillariesPricings',
        validate=validate.Length(min=1),
        metadata={'description': ''}
    )
