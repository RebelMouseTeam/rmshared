from typing import Dict
from typing import FrozenSet
from typing import Type
from typing import TypeVar
from typing import get_origin

from rmshared.content.taxonomy.protocols import composites
from rmshared.content.taxonomy.protocols.abc import ILabels

Label = TypeVar('Label')


class Labels(ILabels[Label], composites.ILabels[Label]):
    def __init__(self):
        self.label_type_to_protocol_map: Dict[Type[Label], composites.ILabels.IProtocol[Label]] = dict()
        self.label_keys_to_label_type_map: Dict[FrozenSet[str], Type[Label]] = dict()

    def add_label(self, label_type, protocol):
        label_type = get_origin(label_type) or label_type
        self.label_type_to_protocol_map[label_type] = protocol
        self.label_keys_to_label_type_map[frozenset(protocol.get_keys())] = label_type

    def make_label(self, data):
        label_keys = frozenset(data.keys())
        label_type = self.label_keys_to_label_type_map[label_keys]
        protocol = self.label_type_to_protocol_map[label_type]
        return protocol.make_label(data)

    def jsonify_label(self, label):
        protocol = self.label_type_to_protocol_map[type(label)]
        return protocol.jsonify_label(label)
