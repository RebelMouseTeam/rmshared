from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import Sequence
from typing import TypeVar

from rmshared.content.taxonomy.core.variables.abc import Cases
from rmshared.content.taxonomy.core.variables.abc import Reference

DelegateFilter = TypeVar('DelegateFilter')


class Filter(Generic[DelegateFilter], metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Core(Filter[DelegateFilter]):
    delegates: Sequence[DelegateFilter]


@dataclass(frozen=True)
class Switch(Filter[DelegateFilter]):
    ref: Reference
    cases: Cases[Sequence[DelegateFilter]]
