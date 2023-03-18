from typing import Iterable
from typing import Type

from rmshared.content.taxonomy.protocols.abc import IFields


class Fields(IFields):
    def __init__(self, delegate: IFields, fallback: IFields, exceptions: Iterable[Type[Exception]] = (LookupError, ValueError, TypeError)):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def make_field(self, data):
        try:
            return self.delegate.make_field(data)
        except self.exceptions:
            return self.fallback.make_field(data)

    def jsonify_field(self, field):
        try:
            return self.delegate.jsonify_field(field)
        except self.exceptions:
            return self.fallback.jsonify_field(field)
