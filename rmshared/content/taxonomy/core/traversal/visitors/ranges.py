from typing import Any

from rmshared.content.taxonomy.core.traversal.visitors.abc import IRanges


class Ranges(IRanges):
    def __init__(self, delegate: Any):
        self.delegate = delegate

    def visit_range(self, range_):
        if isinstance(self.delegate, IRanges):
            return self.delegate.visit_range(range_)
        else:
            return None
