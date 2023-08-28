from abc import ABCMeta
from dataclasses import dataclass
from typing import Optional

from rmshared.dataclasses import total_ordering


@dataclass(frozen=True)
@total_ordering
class Guid(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Event(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Metric:
    event: Event
    count: float
    value: Optional[float]
