from typing import Iterable

from rmshared.content.taxonomy.visitors.abc import IValues


class Values(IValues):
    def __init__(self, delegate: IValues, fallback: IValues, exceptions: Iterable[Exception] = (LookupError, ValueError, TypeError)):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def visit_value(self, value):
        try:
            return self.delegate.visit_value(value)
        except self.exceptions:
            return self.fallback.visit_value(value)
