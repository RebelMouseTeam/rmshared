from rmshared.content.taxonomy import protocols
from rmshared.content.taxonomy.core2 import orders


class Value(protocols.builders.IOrders.IProtocol[orders.Value]):
    def __init__(self, fields: protocols.IFields):
        self.fields = fields

    @classmethod
    def get_name(cls):
        return 'value'

    def make_order(self, info):
        return orders.Value(
            field=self.fields.make_field(info['field']),
            reverse=bool(info['reverse']),
        )

    def jsonify_order_info(self, order_: orders.Value):
        return {
            'field': self.fields.jsonify_field(order_.field),
            'reverse': order_.reverse,
        }
