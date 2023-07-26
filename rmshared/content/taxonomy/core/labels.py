from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from rmshared.dataclasses import total_ordering

Field = TypeVar('Field')
Value = TypeVar('Value')


@dataclass(frozen=True)
@total_ordering
class Label(Generic[Field], metaclass=ABCMeta):
    field: Field


@dataclass(frozen=True)
@total_ordering
class Value(Label[Field], Generic[Field, Value]):
    value: Value


@dataclass(frozen=True)
@total_ordering
class Badge(Label[Field]):
    pass


@dataclass(frozen=True)
@total_ordering
class Empty(Label[Field]):
    pass
