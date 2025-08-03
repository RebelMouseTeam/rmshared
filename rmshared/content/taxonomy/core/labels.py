from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from rmshared.dataclasses import total_ordering

Field = TypeVar('Field')
Scalar = TypeVar('Scalar')


@dataclass(frozen=True)
@total_ordering
class Label(Generic[Field], metaclass=ABCMeta):
    field: Field


@dataclass(frozen=True)
@total_ordering
class Value(Label[Field], Generic[Field, Scalar]):
    value: Scalar


@dataclass(frozen=True)
@total_ordering
class Badge(Label[Field]):
    pass


@dataclass(frozen=True)
@total_ordering
class Empty(Label[Field]):
    pass
