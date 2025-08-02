from typing import Any

from rmshared.content.taxonomy.core.traversal.visitors.abc import IFields


class Fields(IFields):
    def __init__(self, delegate: Any):
        self.delegate = delegate

    def visit_field(self, field):
        isinstance(self.delegate, IFields) and self.delegate.visit_field(field)
