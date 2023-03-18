from typing import Iterable
from typing import Type

from rmshared.content.taxonomy.protocols.abc import IValues


class Values(IValues):
    def __init__(self, delegate: IValues, fallback: IValues, exceptions: Iterable[Type[Exception]] = (LookupError, ValueError, TypeError)):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def make_value(self, data):
        try:
            return self.delegate.make_value(data)
        except self.exceptions:
            return self.fallback.make_value(data)

    def jsonify_value(self, value):
        try:
            return self.delegate.jsonify_value(value)
        except self.exceptions:
            return self.fallback.jsonify_value(value)
