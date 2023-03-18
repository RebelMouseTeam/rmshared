from typing import Iterable
from typing import Type

from rmshared.content.taxonomy.protocols.abc import IFilters


class Filters(IFilters):
    def __init__(self, delegate: IFilters, fallback: IFilters, exceptions: Iterable[Type[Exception]] = (LookupError, ValueError, TypeError)):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def make_filter(self, data):
        try:
            return self.delegate.make_filter(data)
        except self.exceptions:
            return self.fallback.make_filter(data)

    def jsonify_filter(self, filter_):
        try:
            return self.delegate.jsonify_filter(filter_)
        except self.exceptions:
            return self.fallback.jsonify_filter(filter_)
