from typing import Iterable
from typing import Type

from rmshared.content.taxonomy.protocols.abc import IRanges


class Ranges(IRanges):
    def __init__(self, delegate: IRanges, fallback: IRanges, exceptions: Iterable[Type[Exception]] = (LookupError, ValueError, TypeError)):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def make_range(self, data):
        try:
            return self.delegate.make_range(data)
        except self.exceptions:
            return self.fallback.make_range(data)

    def jsonify_range(self, range_):
        try:
            return self.delegate.jsonify_range(range_)
        except self.exceptions:
            return self.fallback.jsonify_range(range_)
