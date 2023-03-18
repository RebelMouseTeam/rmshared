from typing import Iterable
from typing import Type

from rmshared.content.taxonomy.visitors.abc import IFields


class Fields(IFields):
    def __init__(self, delegate: IFields, fallback: IFields, exceptions: Iterable[Type[Exception]]):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def visit_field(self, field):
        try:
            return self.delegate.visit_field(field)
        except self.exceptions:
            return self.fallback.visit_field(field)
