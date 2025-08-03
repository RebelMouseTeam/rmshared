from typing import Any

from rmshared.content.taxonomy.core.traversal.visitors.abc import ILabels


class Labels(ILabels):
    def __init__(self, delegate: Any):
        self.delegate = delegate

    def visit_label(self, label):
        if isinstance(self.delegate, ILabels):
            return self.delegate.visit_label(label)
        else:
            return None
