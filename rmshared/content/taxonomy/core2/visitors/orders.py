from typing import TypeVar

from rmshared.content.taxonomy import visitors
from rmshared.content.taxonomy.core2 import orders

Order = TypeVar('Order')
InField = TypeVar('InField')
OutField = TypeVar('OutField')


class AsIs(visitors.IOrders[Order, Order]):
    def visit_order(self, order):
        return order


class MapValue(visitors.IOrders[orders.Value[InField], orders.Value[OutField]]):
    def __init__(self, fields: visitors.IFields[InField, OutField]):
        self.fields = fields

    def visit_order(self, order: orders.Value[InField]) -> orders.Value[OutField]:
        field = self.fields.visit_field(order.field)
        return orders.Value(field, reverse=order.reverse)
