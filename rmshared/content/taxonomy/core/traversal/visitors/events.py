from typing import Any

from rmshared.content.taxonomy.core.traversal.visitors.abc import IEvents


class Events(IEvents):
    def __init__(self, delegate: Any):
        self.delegate = delegate

    def enter_event(self, event):
        isinstance(self.delegate, IEvents) and self.delegate.enter_event(event)

    def leave_event(self, event):
        isinstance(self.delegate, IEvents) and self.delegate.leave_event(event)
