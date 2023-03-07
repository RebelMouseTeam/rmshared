from typing import TypeVar

from rmshared.content.taxonomy.core2.protocols.abc import IValues

Scalar = TypeVar('Scalar', str, int, float)


class Values(IValues[Scalar]):
    def make_value(self, data):
        assert isinstance(data, (str, int, float))
        return data

    def jsonify_value(self, value):
        assert isinstance(value, (str, int, float))
        return value
