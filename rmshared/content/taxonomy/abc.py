from abc import ABCMeta
from dataclasses import dataclass
from typing import AbstractSet
from typing import Any
from typing import Generic
from typing import Mapping
from typing import Optional
from typing import TypeVar

Scalar = TypeVar('Scalar', str, int, float)


class Guid(metaclass=ABCMeta):
    pass


class Text(metaclass=ABCMeta):
    pass


class Label(metaclass=ABCMeta):
    pass


class Field(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Value(Generic[Scalar]):
    field: 'Field'
    value: Scalar


@dataclass(frozen=True)
class Range(Generic[Scalar]):
    field: 'Field'
    min_value: Optional[Scalar]
    max_value: Optional[Scalar]


@dataclass(frozen=True)
class Aspects:
    texts: AbstractSet['Text']
    labels: AbstractSet['Label']
    values: AbstractSet['Value']
    extras: Mapping[str, Any]


@dataclass(frozen=True)
class Entity:
    guid: 'Guid'
    aspects: Optional['Aspects']


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


class Order(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Chunk:
    order: 'Order'
    limit: int
    offset: int
    cursor: Optional[str]


class Grouping(metaclass=ABCMeta):
    pass
