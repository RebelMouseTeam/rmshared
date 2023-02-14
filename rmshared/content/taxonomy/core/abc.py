from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from typing import AbstractSet
from typing import Generic
from typing import Iterable
from typing import TypeVar

Scalar = TypeVar('Scalar', str, int, float)


class Filter(metaclass=ABCMeta):
    pass


class Label(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Value(metaclass=ABCMeta):
    field: 'Field'
    value: Scalar


class Range(Generic[Scalar], metaclass=ABCMeta):
    pass


class Order(metaclass=ABCMeta):
    pass


class Field(metaclass=ABCMeta):
    pass


class IMatcher(metaclass=ABCMeta):
    @abstractmethod
    def do_aspects_match_filters(self, aspects: 'IMatcher.IAspects', filters_: Iterable['Filter']) -> bool:
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
