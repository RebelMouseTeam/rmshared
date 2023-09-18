from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy import core

Case = TypeVar('Case')
Index = TypeVar('Index')
Scalar = TypeVar('Scalar')
InFilter = TypeVar('InFilter')
OutFilter = TypeVar('OutFilter')

Filter = TypeVar('Filter')
Label = TypeVar('Label')
Range = TypeVar('Range')
Field = TypeVar('Field')
Event = TypeVar('Event')


@dataclass(frozen=True)
class Operator(Generic[Case], metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Argument(Generic[Scalar], metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Reference:
    alias: str


class IResolver(Generic[InFilter, OutFilter], metaclass=ABCMeta):
    @abstractmethod
    def dereference_filters(self, filters_: Iterable[InFilter], arguments_: 'IResolver.IArguments') -> Iterator[OutFilter]:
        pass

    class IArguments(metaclass=ABCMeta):
        @abstractmethod
        def get_argument(self, alias: str) -> 'Argument':
            pass

        @abstractmethod
        def get_value(self, alias: str, index: int) -> Scalar:
            pass


class IProtocol(core.protocols.IComposite[Operator[Filter], Operator[Label], Operator[Range], Field, Event, Scalar], metaclass=ABCMeta):
    @abstractmethod
    def make_argument(self, data: str) -> Type[Argument]:
        pass

    @abstractmethod
    def jsonify_argument(self, argument: Type[Argument]) -> str:
        pass
