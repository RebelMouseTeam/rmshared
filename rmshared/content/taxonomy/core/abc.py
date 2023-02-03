from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from typing import AbstractSet
from typing import Generic
from typing import TypeVar

Field = str
Scalar = TypeVar('Scalar', str, int, float)


@dataclass(frozen=True)
class Entity(metaclass=ABCMeta):
    name: str


@dataclass(frozen=True)
class Guid(Generic[Scalar], metaclass=ABCMeta):
    entity: 'Entity'
    id: Scalar


class Label(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Value(metaclass=ABCMeta):
    field: Field
    value: Scalar


class Range(Generic[Scalar], metaclass=ABCMeta):
    pass


class Filter(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Order:
    field: Field
    reverse: bool


class IMatcher(metaclass=ABCMeta):
    @abstractmethod
    def do_aspects_match_filters(self, aspects: 'IMatcher.IAspects', filters_: AbstractSet['Filter']) -> bool:
        pass

    class IAspects(metaclass=ABCMeta):
        @property
        @abstractmethod
        def labels(self) -> AbstractSet['Label']:
            pass

        @property
        @abstractmethod
        def values(self) -> AbstractSet['Value']:
            pass
