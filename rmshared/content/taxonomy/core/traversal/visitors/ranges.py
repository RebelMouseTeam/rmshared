from typing import Any

from rmshared.content.taxonomy.core.traversal.visitors.abc import IRanges


class Ranges(IRanges):
    def __init__(self, delegate: Any):
        self.delegate = delegate

    def enter_range(self, range_):
        isinstance(self.delegate, IRanges) and self.delegate.enter_range(range_)

    def leave_range(self, range_):
        isinstance(self.delegate, IRanges) and self.delegate.leave_range(range_)
