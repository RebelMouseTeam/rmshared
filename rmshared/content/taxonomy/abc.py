from abc import ABCMeta
from dataclasses import dataclass

from rmshared.dataclasses import total_ordering


@dataclass(frozen=True)
@total_ordering
class Guid(metaclass=ABCMeta):
    pass


class Event(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Metric:
    event: Event
    count: float
