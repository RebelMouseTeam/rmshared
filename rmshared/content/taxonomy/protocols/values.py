from operator import methodcaller
from typing import Callable
from typing import Tuple
from typing import TypeVar

from rmshared.content.taxonomy.protocols import builders
from rmshared.content.taxonomy.protocols.abc import IValues

Value = TypeVar('Value')


class Values(IValues[Value], builders.IValues[Value]):
    def __init__(self):
        self.protocols: Tuple[builders.IValues.IProtocol[Value]] = tuple()

    def add_value(self, protocol):
        self.protocols += (protocol,)

    def make_value(self, data):
        return self._try_protocols(methodcaller('make_value', data), error=f'Could not make value from {data}')

    def jsonify_value(self, value):
        return self._try_protocols(methodcaller('jsonify_value', value), error=f'Could not jsonify value {value}')

    Out = TypeVar('Out')

    def _try_protocols(self, func: Callable[[builders.IValues.IProtocol[Value]], Out], error: str) -> Out:
        for protocol in self.protocols:
            try:
                return func(protocol)
            except ValueError:
                pass
        else:
            raise ValueError(error)
