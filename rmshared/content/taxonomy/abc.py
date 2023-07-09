from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import Optional
from typing import TypeVar

from rmshared.dataclasses import total_ordering

Scalar = TypeVar('Scalar', str, int, float)


@dataclass(frozen=True)
@total_ordering
class Guid(metaclass=ABCMeta):
    pass


class Text(metaclass=ABCMeta):
    pass


class Label(metaclass=ABCMeta):
    pass


class Field(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Range(Generic[Scalar]):
    field: 'Field'
    min_value: Optional[Scalar]
    max_value: Optional[Scalar]


class Event(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Metric:
    event: Event
    count: float


class Condition(metaclass=ABCMeta):
    pass


class Filter(metaclass=ABCMeta):
    pass
