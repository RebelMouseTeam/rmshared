from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import Mapping
from typing import Sequence
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy.core2.variables.abc import Argument
from rmshared.content.taxonomy.core2.variables.abc import Reference

Case = TypeVar('Case')


class Operator(Generic[Case], metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Switch(Operator[Case]):
    ref: Reference
    cases: Mapping[Type[Argument], Operator[Case]]


@dataclass(frozen=True)
class Return(Operator[Case]):
    cases: Sequence[Case]
