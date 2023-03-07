from rmshared.content.taxonomy.core2.protocols.abc import IOrders
from rmshared.content.taxonomy.core2.protocols.abc import IFilters
from rmshared.content.taxonomy.core2.protocols.abc import IProtocol


class Protocol(IProtocol):
    def __init__(self, filters: IFilters, orders: IOrders):
        self.filters = filters
        self.orders = orders

    def make_filters(self, data):
        return map(self.filters.make_filter, data)

    def jsonify_filters(self, filters):
        return list(map(self.filters.jsonify_filter, filters))

    def make_order(self, data):
        return self.orders.make_order(data)

    def jsonify_order(self, order):
        return self.orders.jsonify_order(order)
