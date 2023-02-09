from typing import Callable
from typing import Mapping
from typing import Type

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import orders
from rmshared.content.taxonomy.abc import Order
from rmshared.content.taxonomy.mappers.abc import IFields
from rmshared.content.taxonomy.mappers.abc import IOrders


class Orders(IOrders):
    def __init__(self, fields: IFields):
        self.fields = fields
        self.order_order_to_factory_func_map: Mapping[Type[Order], Callable[[Order], core.Order]] = {
            orders.Value: self._map_order_by_value,
            orders.Relevance: NotImplemented,
        }

    def map_order(self, order):
        return self.order_order_to_factory_func_map[type(order)](order)

    def _map_order_by_value(self, order: orders.Value) -> core.orders.Value:
        return core.orders.Value(
            field=self.fields.map_field(order.field),
            reverse=order.reverse,
        )
