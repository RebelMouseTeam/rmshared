from typing import Callable

from rmshared.content.taxonomy.core import events

__all__ = ('Event', )


class Event(Callable[[], events.Event]):
    def __init__(self, name: str):
        self.name = name

    def __hash__(self):
        return (self.__class__, self.name).__hash__()

    def __call__(self) -> events.Event:
        return events.Event(name=self.name)
