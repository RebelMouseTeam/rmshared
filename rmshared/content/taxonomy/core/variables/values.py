from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from rmshared.content.taxonomy.core.variables.abc import Reference

DelegateValue = TypeVar('DelegateValue')


class Value(Generic[DelegateValue], metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Constant(Value[DelegateValue]):
    value: DelegateValue


@dataclass(frozen=True)
class Variable(Value):
    ref: Reference
    index: int
