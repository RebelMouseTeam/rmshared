from typing import Any

from rmshared.content.taxonomy.core.traversal.visitors.abc import ILabels


class Labels(ILabels):
    def __init__(self, delegate: Any):
        self.delegate = delegate

    def enter_label(self, label):
        isinstance(self.delegate, ILabels) and self.delegate.enter_label(label)

    def leave_label(self, label):
        isinstance(self.delegate, ILabels) and self.delegate.leave_label(label)
