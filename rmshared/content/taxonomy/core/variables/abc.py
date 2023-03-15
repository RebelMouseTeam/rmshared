from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import TypeVar

from rmshared.content.taxonomy.core.variables import arguments

Scalar = TypeVar('Scalar')
InFilter = TypeVar('InFilter')
OutFilter = TypeVar('OutFilter')


@dataclass(frozen=True)
class Reference:
    alias: str


class IResolver(Generic[InFilter, OutFilter], metaclass=ABCMeta):
    @abstractmethod
    def dereference_filters(self, filters_: Iterable[InFilter], arguments_: 'IResolver.IArguments') -> Iterator[OutFilter]:
        pass

    class IArguments(metaclass=ABCMeta):
        @abstractmethod
        def get_argument(self, alias: str) -> 'arguments.Argument':
            pass

        @abstractmethod
        def get_value(self, alias: str, index: int) -> Scalar:
            pass
