from typing import Iterable

from rmshared.content.taxonomy.visitors.abc import ILabels


class Labels(ILabels):
    def __init__(self, delegate: ILabels, fallback: ILabels, exceptions: Iterable[Exception] = (LookupError, ValueError, TypeError)):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def visit_label(self, label):
        try:
            return self.delegate.visit_label(label)
        except self.exceptions:
            return self.fallback.visit_label(label)
