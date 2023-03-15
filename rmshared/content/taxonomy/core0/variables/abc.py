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

from rmshared.content.taxonomy.core0 import server as core0_server
from rmshared.content.taxonomy.core0.abc import Scalar
from rmshared.content.taxonomy.core0.abc import Filter

Case = TypeVar('Case')


@dataclass(frozen=True)
@total_ordering
class Argument(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Cases(Generic[Case]):
    cases: Mapping[Type['Argument'], Case]


@dataclass(frozen=True)
class Constant(Generic[Scalar]):
    value: Scalar


@dataclass(frozen=True)
class Reference:
    alias: str


@dataclass(frozen=True)
class Variable:
    ref: 'Reference'
    index: int


class IResolver(metaclass=ABCMeta):
    @abstractmethod
    def dereference_filters(self, filters_: Iterable[Filter], arguments: 'IResolver.IArguments') -> Iterator[Filter]:
        pass

    class IArguments(metaclass=ABCMeta):
        @abstractmethod
        def get_argument(self, alias: str) -> 'Argument':
            pass

        @abstractmethod
        def get_value(self, alias: str, index: int) -> Scalar:
            pass


class IProtocol(core0_server.IProtocol, metaclass=ABCMeta):
    @abstractmethod
    def make_argument(self, data: str) -> Type[Argument]:
        pass

    @abstractmethod
    def jsonify_argument(self, argument: Type[Argument]) -> str:
        pass
