from typing import Dict
from typing import Type
from typing import TypeVar

from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.protocols import builders
from rmshared.content.taxonomy.protocols.abc import IFilters

Filter = TypeVar('Filter')


class Filters(IFilters[Filter], builders.IFilters[Filter]):
    def __init__(self):
        self.filter_to_protocol_map: Dict[Type[Filter], builders.IFilters.IProtocol] = dict()
        self.filter_name_to_filter_map: Dict[str, Type[Filter]] = dict()

    def add_filter(self, filter_type, protocol):
        self.filter_to_protocol_map[filter_type] = protocol
        self.filter_name_to_filter_map[protocol.get_name()] = filter_type

    def make_filter(self, data):
        name, info = parse_name_and_info(data)
        filter_type = self.filter_name_to_filter_map[name]
        protocol = self.filter_to_protocol_map[filter_type]
        return protocol.make_filter(info)

    def jsonify_filter(self, filter_):
        protocol = self.filter_to_protocol_map[type(filter_)]
        name = protocol.get_name()
        info = protocol.jsonify_filter_info(filter_)
        return {name: info}
