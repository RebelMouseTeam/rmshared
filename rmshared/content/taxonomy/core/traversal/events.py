from typing import Any

from rmshared.content.taxonomy.core.traversal import visitors
from rmshared.content.taxonomy.core.traversal.abc import IEvents


class Events(IEvents):
    def traverse_events(self, events_, visitor):
        for event in events_:
            self._visit_event(event, visitor=visitors.Events(delegate=visitor))

    @staticmethod
    def _visit_event(event: Any, visitor: visitors.IEvents) -> None:
        visitor.visit_event(event)
