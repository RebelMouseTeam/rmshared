from typing import TypeVar

from rmshared.content.taxonomy.core import events
from rmshared.content.taxonomy.core.encoders.abc import IEvents

Event = TypeVar('Event', bound=events.Event)


class Events(IEvents[events.Event, str]):
    def encode_event(self, event: events.Event):
        return event.name
