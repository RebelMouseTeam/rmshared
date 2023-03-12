from typing import Iterable

from rmshared.content.taxonomy.visitors.abc import IFilters


class Filters(IFilters):
    def __init__(self, delegate: IFilters, fallback: IFilters, exceptions: Iterable[Exception] = (LookupError, ValueError, TypeError)):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def visit_filter(self, filter_):
        try:
            return self.delegate.visit_filter(filter_)
        except self.exceptions:
            return self.fallback.visit_filter(filter_)
