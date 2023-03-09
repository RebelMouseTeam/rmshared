from typing import Dict
from typing import FrozenSet
from typing import Type
from typing import TypeVar

from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.protocols import builders
from rmshared.content.taxonomy.protocols.abc import IFields

Field = TypeVar('Field')


class Fields(IFields[Field], builders.IFields[Field]):
    def __init__(self):
        self.field_to_protocol_map: Dict[Type[Field], builders.IFields.IProtocol] = dict()
        self.field_keys_to_field_map: Dict[FrozenSet[str], Type[Field]] = dict()

    def add_field(self, field_type, protocol):
        self.field_to_protocol_map[field_type] = protocol
        self.field_keys_to_field_map[frozenset(protocol.get_keys())] = field_type

    def make_field(self, data):
        name, info = parse_name_and_info(data)
        field_keys = frozenset(info.keys())
        field_type = self.field_keys_to_field_map[field_keys]
        protocol = self.field_to_protocol_map[field_type]
        return protocol.make_field(name, info)

    def jsonify_field(self, field_):
        protocol = self.field_to_protocol_map[type(field_)]
        name, info = protocol.jsonify_field(field_)
        return {name: info}
