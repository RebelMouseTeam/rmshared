from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from typing import AbstractSet
from typing import Any
from typing import Generic
from typing import Iterable
from typing import Mapping
from typing import Optional
from typing import TypeVar

Scalar = TypeVar('Scalar', str, int, float)


@dataclass(frozen=True)
class Aspects:
    labels: AbstractSet['Label']
    values: AbstractSet['Value']
    extras: Mapping[str, Any]


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
        @abstractmethod
        def does_have_label(self, label: 'Label') -> bool:
            pass

        @abstractmethod
        def get_value_or_none(self, field: 'Field') -> Optional['Scalar']:
            pass
