from typing import Dict
from typing import FrozenSet
from typing import Type
from typing import TypeVar
from typing import get_origin

from rmshared.content.taxonomy.protocols import composites
from rmshared.content.taxonomy.protocols.abc import IOrders

Order = TypeVar('Order')


class Orders(IOrders[Order], composites.IOrders[Order]):
    def __init__(self):
        self.order_type_to_protocol_map: Dict[Type[Order], composites.IOrders.IProtocol[Order]] = dict()
        self.order_keys_to_order_type_map: Dict[FrozenSet[str], Type[Order]] = dict()

    def add_order(self, order_type, protocol):
        order_type = get_origin(order_type) or order_type
        self.order_type_to_protocol_map[order_type] = protocol
        self.order_keys_to_order_type_map[frozenset(protocol.get_keys())] = order_type

    def make_order(self, data):
        order_keys = frozenset(data.keys())
        order_type = self.order_keys_to_order_type_map[order_keys]
        protocol = self.order_type_to_protocol_map[order_type]
        return protocol.make_order(data)

    def jsonify_order(self, order):
        protocol = self.order_type_to_protocol_map[type(order)]
        return protocol.jsonify_order(order)
