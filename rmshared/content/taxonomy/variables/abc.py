from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import Tuple
from typing import TypeVar

Case = TypeVar('Case')
Scalar = TypeVar('Scalar')
Filter = TypeVar('Filter')


@dataclass(frozen=True)
class Operator(Generic[Case], metaclass=ABCMeta):
    ...


@dataclass(frozen=True)
class Argument(Generic[Scalar], metaclass=ABCMeta):
    ...


@dataclass(frozen=True)
class Reference:
    alias: str


class IResolver(metaclass=ABCMeta):
    @abstractmethod
    def dereference_filters(self, operators_: Iterable[Operator[Filter]], arguments_: IArguments) -> Iterator[Filter]: ...

    @abstractmethod
    def dereference_filters_partially(
            self, operators_: Iterable[Operator[Filter]], arguments_: IArguments) -> Tuple[Iterable[Filter], Iterable[Operator[Filter]]]: ...

    class IArguments(metaclass=ABCMeta):
        @abstractmethod
        def get_argument(self, alias: str) -> Argument:  # :raises: ArgumentNotFoundException
            ...

        class ArgumentNotFoundException(LookupError):
            ...
