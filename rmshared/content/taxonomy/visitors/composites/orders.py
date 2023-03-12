from typing import Mapping
from typing import NoReturn
from typing import Type
from typing import TypeVar
from typing import get_origin

from rmshared.content.taxonomy.visitors.abc import IOrders

InOrder = TypeVar('InOrder')
OutOrder = TypeVar('OutOrder')


class Orders(IOrders[InOrder, OutOrder]):
    def __init__(self, order_to_visitor_map: Mapping[Type[InOrder], IOrders[InOrder, OutOrder]] = None):
        self.order_to_visitor_map = dict(order_to_visitor_map or dict())

    def add_order(self, order_type: Type[InOrder], visitor: IOrders) -> NoReturn:
        self.order_to_visitor_map[get_origin(order_type) or order_type] = visitor

    def visit_order(self, order: InOrder) -> OutOrder:
        return self.order_to_visitor_map[type(order)].visit_order(order)
