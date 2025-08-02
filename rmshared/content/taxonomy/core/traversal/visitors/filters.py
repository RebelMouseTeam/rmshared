from typing import Any

from rmshared.content.taxonomy.core.traversal.visitors.abc import IFilters


class Filters(IFilters):
    def __init__(self, delegate: Any):
        self.delegate = delegate

    def enter_filter(self, filter_):
        isinstance(self.delegate, IFilters) and self.delegate.enter_filter(filter_)

    def leave_filter(self, filter_):
        isinstance(self.delegate, IFilters) and self.delegate.leave_filter(filter_)
