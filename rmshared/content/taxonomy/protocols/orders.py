from typing import Dict
from typing import Type
from typing import TypeVar

from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.protocols import builders
from rmshared.content.taxonomy.protocols.abc import IOrders

Order = TypeVar('Order')


class Orders(IOrders[Order], builders.IOrders[Order]):
    def __init__(self):
        self.order_to_protocol_map: Dict[Type[Order], builders.IOrders.IProtocol[Order]] = dict()
        self.order_name_to_order_map: Dict[str, Type[Order]] = dict()

    def add_order(self, order_type, protocol):
        self.order_to_protocol_map[order_type] = protocol
        self.order_name_to_order_map[protocol.get_name()] = order_type

    def make_order(self, data):
        name, info = parse_name_and_info(data)
        order_type = self.order_name_to_order_map[name]
        protocol = self.order_to_protocol_map[order_type]
        return protocol.make_order(info)

    def jsonify_order(self, order_):
        protocol = self.order_to_protocol_map[type(order_)]
        name = protocol.get_name()
        info = protocol.jsonify_order_info(order_)
        return {name: info}
