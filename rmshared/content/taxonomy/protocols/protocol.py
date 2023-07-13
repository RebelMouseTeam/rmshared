from rmshared.content.taxonomy.protocols.abc import IFilters
from rmshared.content.taxonomy.protocols.abc import IOrders
from rmshared.content.taxonomy.protocols.abc import IFields
from rmshared.content.taxonomy.protocols.abc import IProtocol


class Protocol(IProtocol):
    def __init__(self, filters: IFilters, orders: IOrders, fields: IFields):
        self.filters = filters
        self.orders = orders
        self.fields = fields

    def make_filters(self, data):
        return map(self.filters.make_filter, data)

    def jsonify_filters(self, filters_):
        return list(map(self.filters.jsonify_filter, filters_))

    def make_filter(self, data):
        return self.filters.make_filter(data)

    def jsonify_filter(self, filter_):
        return self.filters.jsonify_filter(filter_)

    def make_order(self, data):
        return self.orders.make_order(data)

    def jsonify_order(self, order):
        return self.orders.jsonify_order(order)

    def make_field(self, data):
        return self.fields.make_field(data)

    def jsonify_field(self, field):
        return self.fields.jsonify_field(field)

    def make_event(self, data):
        raise NotImplementedError('No events yet')

    def jsonify_event(self, event):
        raise NotImplementedError('No events yet')
