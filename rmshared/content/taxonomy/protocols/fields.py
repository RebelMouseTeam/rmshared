from typing import Dict
from typing import FrozenSet
from typing import Type
from typing import TypeVar
from typing import get_origin

from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.protocols import composites
from rmshared.content.taxonomy.protocols.abc import IFields

Field = TypeVar('Field')


class Fields(IFields[Field], composites.IFields[Field]):
    def __init__(self):
        self.field_type_to_protocol_map: Dict[Type[Field], composites.IFields.IProtocol] = dict()
        self.field_keys_to_field_type_map: Dict[FrozenSet[str], Type[Field]] = dict()

    def add_field(self, field_type, protocol):
        field_type = get_origin(field_type) or field_type
        self.field_type_to_protocol_map[field_type] = protocol
        self.field_keys_to_field_type_map[frozenset(protocol.get_keys())] = field_type

    def make_field(self, data):
        name, info = parse_name_and_info(data)
        field_keys = frozenset(info.keys())
        field_type = self.field_keys_to_field_type_map[field_keys]
        protocol = self.field_type_to_protocol_map[field_type]
        return protocol.make_field(name, info)

    def jsonify_field(self, field):
        protocol = self.field_type_to_protocol_map[type(field)]
        name, info = protocol.jsonify_field(field)
        return {name: info}
