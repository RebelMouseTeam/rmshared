from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

Field = TypeVar('Field')
Value = TypeVar('Value')


@dataclass(frozen=True)
class Range(Generic[Field], metaclass=ABCMeta):
    field: Field


@dataclass(frozen=True)
class Between(Range[Field], Generic[Field, Value]):
    min_value: Value
    max_value: Value


@dataclass(frozen=True)
class LessThan(Range[Field], Generic[Field, Value]):
    value: Value


@dataclass(frozen=True)
class MoreThan(Range[Field], Generic[Field, Value]):
    value: Value
