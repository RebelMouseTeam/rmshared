"""
TODO: probably just drop it all!

from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import TypeVar


@dataclass(frozen=True)
class Aspects:
    labels: AbstractSet['Label']
    values: AbstractSet['Value']
    extras: Mapping[str, Any]


@dataclass(frozen=True)
class Value(metaclass=ABCMeta):
    field: 'Field'
    value: Scalar


Filter = TypeVar('Filter')
Label = TypeVar('Label')
Field = TypeVar('Field')
Value = TypeVar('Value')


class IMatcher(Generic[Filter, Label, Field, Value], metaclass=ABCMeta):
    @abstractmethod
    def do_aspects_match_filters(self, aspects: 'IMatcher.IAspects', filters_: Iterable['Filter']) -> bool:
        pass

    class IAspects(metaclass=ABCMeta):
        @abstractmethod
        def get_labels(self, field: 'Field') -> Iterator['Label']:
            pass

        @abstractmethod
        def get_values(self, field: 'Field') -> Iterator['Value']:
            pass
"""
