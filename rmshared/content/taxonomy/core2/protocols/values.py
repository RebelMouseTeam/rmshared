from typing import AbstractSet
from typing import TypeVar

from rmshared.content.taxonomy import protocols


class Scalar(protocols.builders.IValues.IProtocol[str | int | float]):
    V = TypeVar('V', str, int, float)

    def __init__(self, value_types: AbstractSet[str | int | float]):
        self.value_types = tuple(value_types)

    def make_value(self, data):
        return self._assert_value_type(data)

    def jsonify_value(self, value):
        return self._assert_value_type(value)

    def _assert_value_type(self, data: V) -> V:
        if isinstance(data, self.value_types):
            return data
        else:
            raise ValueError(f'Expected one of {self.value_types}, got {data}')
