from typing import Dict
from typing import FrozenSet
from typing import Type
from typing import TypeVar
from typing import get_origin

from rmshared.content.taxonomy.protocols import composites
from rmshared.content.taxonomy.protocols.abc import IFilters

Filter = TypeVar('Filter')


class Filters(IFilters[Filter], composites.IFilters[Filter]):
    def __init__(self):
        self.filter_type_to_protocol_map: Dict[Type[Filter], composites.IFilters.IProtocol] = dict()
        self.filter_keys_to_filter_type_map: Dict[FrozenSet[str], Type[Filter]] = dict()

    def add_filter(self, filter_type, protocol):
        filter_type = get_origin(filter_type) or filter_type
        self.filter_type_to_protocol_map[filter_type] = protocol
        self.filter_keys_to_filter_type_map[frozenset(protocol.get_keys())] = filter_type

    def make_filter(self, data):
        filter_keys = frozenset(data.keys())
        filter_type = self.filter_keys_to_filter_type_map[filter_keys]
        protocol = self.filter_type_to_protocol_map[filter_type]
        return protocol.make_filter(data)

    def jsonify_filter(self, filter_):
        protocol = self.filter_type_to_protocol_map[type(filter_)]
        return protocol.jsonify_filter(filter_)
