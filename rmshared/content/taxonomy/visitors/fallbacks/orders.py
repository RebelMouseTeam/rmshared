from typing import Iterable
from typing import Type

from rmshared.content.taxonomy.visitors.abc import IOrders


class Orders(IOrders):
    def __init__(self, delegate: IOrders, fallback: IOrders, exceptions: Iterable[Type[Exception]]):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def visit_order(self, order):
        try:
            return self.delegate.visit_order(order)
        except self.exceptions:
            return self.fallback.visit_order(order)
