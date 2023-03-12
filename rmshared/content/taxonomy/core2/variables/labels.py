from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import Sequence
from typing import TypeVar

from rmshared.content.taxonomy.core2.variables.abc import Cases
from rmshared.content.taxonomy.core2.variables.abc import Reference

DelegateLabel = TypeVar('DelegateLabel')


class Label(Generic[DelegateLabel], metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Core(Label[DelegateLabel]):
    delegates: Sequence[DelegateLabel]


@dataclass(frozen=True)
class Switch(Label[DelegateLabel]):
    ref: Reference
    cases: Cases[Sequence[DelegateLabel]]
