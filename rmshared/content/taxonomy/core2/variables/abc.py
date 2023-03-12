from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.dataclasses import total_ordering

Case = TypeVar('Case')
Scalar = TypeVar('Scalar')
InFilter = TypeVar('InFilter')
OutFilter = TypeVar('OutFilter')


@dataclass(frozen=True)
@total_ordering
class Argument(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Cases(Generic[Case]):
    cases: Mapping[Type['Argument'], Case]


@dataclass(frozen=True)
class Reference:
    alias: str


class IResolver(Generic[InFilter, OutFilter], metaclass=ABCMeta):
    @abstractmethod
    def dereference_filters(self, filters_: Iterable[InFilter], arguments: 'IResolver.IArguments') -> Iterator[OutFilter]:
        pass

    class IArguments(metaclass=ABCMeta):
        @abstractmethod
        def get_argument(self, alias: str) -> 'Argument':
            pass

        @abstractmethod
        def get_value(self, alias: str, index: int) -> Scalar:
            pass
