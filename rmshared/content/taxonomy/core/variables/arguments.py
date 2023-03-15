from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import Sequence
from typing import TypeVar

Scalar = TypeVar('Scalar')


@dataclass(frozen=True)
class Argument(Generic[Scalar], metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Value(Argument[Scalar]):
    values: Sequence[Scalar]


@dataclass(frozen=True)
class Empty(Argument):
    pass


@dataclass(frozen=True)
class Any(Argument):
    pass
