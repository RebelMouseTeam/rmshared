from typing import Dict
from typing import FrozenSet
from typing import Type
from typing import TypeVar
from typing import get_origin

from rmshared.content.taxonomy.protocols import composites
from rmshared.content.taxonomy.protocols.abc import IRanges

Range = TypeVar('Range')


class Ranges(IRanges[Range], composites.IRanges[Range]):
    def __init__(self):
        self.range_type_to_protocol_map: Dict[Type[Range], composites.IRanges.IProtocol] = dict()
        self.range_keys_to_range_type_map: Dict[FrozenSet[str], Type[Range]] = dict()

    def add_range(self, range_type, protocol):
        range_type = get_origin(range_type) or range_type
        self.range_type_to_protocol_map[range_type] = protocol
        self.range_keys_to_range_type_map[frozenset(protocol.get_keys())] = range_type

    def make_range(self, data):
        range_keys = frozenset(data.keys())
        range_type = self.range_keys_to_range_type_map[range_keys]
        protocol = self.range_type_to_protocol_map[range_type]
        return protocol.make_range(data)

    def jsonify_range(self, range_):
        protocol = self.range_type_to_protocol_map[type(range_)]
        return protocol.jsonify_range(range_)
