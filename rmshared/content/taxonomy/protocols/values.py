from typing import Tuple
from typing import TypeVar

from rmshared.content.taxonomy.protocols import composites
from rmshared.content.taxonomy.protocols.abc import IValues

Value = TypeVar('Value')


class Values(IValues[Value], composites.IValues[Value]):
    def __init__(self):
        self.protocols: Tuple[composites.IValues.IProtocol[Value]] = tuple()

    def add_value(self, protocol):
        self.protocols += (protocol,)

    def make_value(self, data):
        for protocol in self.protocols:
            try:
                return protocol.make_value(data)
            except ValueError:
                pass
        else:
            raise ValueError([f'Could not make value from {data}', self.protocols])

    def jsonify_value(self, value):
        for protocol in self.protocols:
            if isinstance(value, tuple(protocol.get_types())):
                return protocol.jsonify_value(value)
        else:
            raise ValueError([f'Could not jsonify {value}', self.protocols])
