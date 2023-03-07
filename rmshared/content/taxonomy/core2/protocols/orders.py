from rmshared.content.taxonomy.core2 import orders
from rmshared.content.taxonomy.core2.protocols.abc import IOrders
from rmshared.content.taxonomy.core2.protocols.abc import IFields


class Orders(IOrders[orders.Order]):
    def __init__(self, fields: IFields):
        self.fields = fields

    def make_order(self, data):
        return orders.Value(
            field=self.fields.make_field(data['value']['field']),
            reverse=bool(data['value']['reverse']),
        )

    def jsonify_order(self, order):
        assert isinstance(order, orders.Value)
        return {'value': {
            'field': self.fields.jsonify_field(order.field),
            'reverse': order.reverse,
        }}
