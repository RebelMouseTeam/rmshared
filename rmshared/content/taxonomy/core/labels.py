from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

Field = TypeVar('Field')
Value = TypeVar('Value')


@dataclass(frozen=True)
class Label(Generic[Field], metaclass=ABCMeta):
    field: Field


@dataclass(frozen=True)
class Value(Label[Field], Generic[Field, Value]):
    value: Value


@dataclass(frozen=True)
class Badge(Label[Field]):
    pass


@dataclass(frozen=True)
class Empty(Label[Field]):
    pass
