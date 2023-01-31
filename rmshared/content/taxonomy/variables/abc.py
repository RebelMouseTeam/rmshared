from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import Iterable
from typing import TypeVar

AnyValue = TypeVar('AnyValue')


@dataclass(frozen=True)
class Variable(Generic[AnyValue], metaclass=ABCMeta):
    scope: NotImplemented
    values: Iterable[AnyValue]
    labels: 'ValuesLabels'


@dataclass(frozen=True)
class ValuesLabels:
    any: bool
    none: bool
