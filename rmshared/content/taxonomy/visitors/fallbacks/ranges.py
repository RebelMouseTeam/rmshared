from typing import Iterable

from rmshared.content.taxonomy.visitors.abc import IRanges


class Ranges(IRanges):
    def __init__(self, delegate: IRanges, fallback: IRanges, exceptions: Iterable[Exception] = (LookupError, ValueError, TypeError)):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def visit_range(self, range_):
        try:
            return self.delegate.visit_range(range_)
        except self.exceptions:
            return self.fallback.visit_range(range_)
