from typing import Any

from rmshared.content.taxonomy.core.traversal import visitors
from rmshared.content.taxonomy.core.traversal.abc import IEvents


class Events(IEvents):
    def traverse_events(self, events_, visitor) -> None:
        for event in events_:
            self._enter_event(event, visitor=visitors.Events(delegate=visitor))
            self._leave_event(event, visitor=visitors.Events(delegate=visitor))

    @staticmethod
    def _enter_event(event: Any, visitor: visitors.IEvents) -> None:
        return visitor.enter_event(event)

    @staticmethod
    def _leave_event(event: Any, visitor: visitors.IEvents) -> None:
        return visitor.leave_event(event)
