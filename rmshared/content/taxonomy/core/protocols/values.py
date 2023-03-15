from typing import AbstractSet
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy import protocols


class Scalar(protocols.composites.IValues.IProtocol[str | int | float]):
    V = TypeVar('V', str, int, float)

    def __init__(self, value_types: AbstractSet[Type[str | int | float]]):
        self.value_types = tuple(value_types)

    def get_types(self):
        return self.value_types

    def make_value(self, data):
        if isinstance(data, self.value_types):
            return data
        else:
            raise ValueError(f'Expected one of {self.value_types}, got {data}')

    def jsonify_value(self, value):
        return value
