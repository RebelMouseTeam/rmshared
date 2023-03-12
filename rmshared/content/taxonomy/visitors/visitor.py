from rmshared.content.taxonomy.visitors.abc import IOrders
from rmshared.content.taxonomy.visitors.abc import IFilters
from rmshared.content.taxonomy.visitors.abc import IVisitor


class Visitor(IVisitor):
    def __init__(self, filters: IFilters, orders: IOrders):
        self.filters = filters
        self.orders = orders

    def visit_filters(self, filters):
        return map(self.filters.visit_filter, filters)

    def visit_order(self, order):
        return self.orders.visit_order(order)
