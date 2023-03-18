from typing import Iterable
from typing import Type

from rmshared.content.taxonomy.protocols.abc import IOrders


class Orders(IOrders):
    def __init__(self, delegate: IOrders, fallback: IOrders, exceptions: Iterable[Type[Exception]]):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def make_order(self, data):
        try:
            return self.delegate.make_order(data)
        except self.exceptions:
            return self.fallback.make_order(data)

    def jsonify_order(self, order):
        try:
            return self.delegate.jsonify_order(order)
        except self.exceptions:
            return self.fallback.jsonify_order(order)
