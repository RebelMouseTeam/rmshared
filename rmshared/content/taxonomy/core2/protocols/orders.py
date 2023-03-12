from rmshared.content.taxonomy import protocols
from rmshared.content.taxonomy.core2 import orders


class Value(protocols.composites.IOrders.IProtocol[orders.Value]):
    def __init__(self, fields: protocols.IFields):
        self.fields = fields

    def get_keys(self):
        return {'value'}

    def make_order(self, data):
        return orders.Value(
            field=self.fields.make_field(data['value']['field']),
            reverse=bool(data['value']['reverse']),
        )

    def jsonify_order(self, order: orders.Value):
        return {'value': {
            'field': self.fields.jsonify_field(order.field),
            'reverse': order.reverse,
        }}
