from typing import Dict
from typing import Type
from typing import TypeVar

from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.protocols import builders
from rmshared.content.taxonomy.protocols.abc import ILabels

Label = TypeVar('Label')


class Labels(ILabels[Label], builders.ILabels[Label]):
    def __init__(self):
        self.label_to_protocol_map: Dict[Type[Label], builders.ILabels.IProtocol[Label]] = dict()
        self.label_name_to_label_map: Dict[str, Type[Label]] = dict()

    def add_label(self, label_type, protocol):
        self.label_to_protocol_map[label_type] = protocol
        self.label_name_to_label_map[protocol.get_name()] = label_type

    def make_label(self, data):
        name, info = parse_name_and_info(data)
        label_type = self.label_name_to_label_map[name]
        protocol = self.label_to_protocol_map[label_type]
        return protocol.make_label(info)

    def jsonify_label(self, label_):
        protocol = self.label_to_protocol_map[type(label_)]
        name = protocol.get_name()
        info = protocol.jsonify_label_info(label_)
        return {name: info}
