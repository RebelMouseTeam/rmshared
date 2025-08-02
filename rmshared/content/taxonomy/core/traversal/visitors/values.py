from typing import Any

from rmshared.content.taxonomy.core.traversal.visitors.abc import IValues


class Values(IValues):
    def __init__(self, delegate: Any):
        self.delegate = delegate

    def visit_value(self, value):
        isinstance(self.delegate, IValues) and self.delegate.visit_value(value)
