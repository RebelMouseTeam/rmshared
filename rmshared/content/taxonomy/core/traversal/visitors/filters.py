from typing import Any

from rmshared.content.taxonomy.core.traversal.visitors.abc import IFilters


class Filters(IFilters):
    def __init__(self, delegate: Any):
        self.delegate = delegate

    def visit_filter(self, filter_):
        if isinstance(self.delegate, IFilters):
            return self.delegate.visit_filter(filter_)
        else:
            return None
