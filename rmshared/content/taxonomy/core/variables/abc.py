from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import Mapping
from typing import TypeVar

from rmshared.dataclasses import total_ordering

from rmshared.content.taxonomy.core.abc import Scalar

Case = TypeVar('Case')


@dataclass(frozen=True)
@total_ordering
class Argument(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Cases(Generic[Case]):
    cases: Mapping['Argument', Case]


@dataclass(frozen=True)
class Constant(Generic[Scalar]):
    value: Scalar


@dataclass(frozen=True)
class Reference:
    alias: str


@dataclass(frozen=True)
class Variable:
    ref: 'Reference'
    index: int
