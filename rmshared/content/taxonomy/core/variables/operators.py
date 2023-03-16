from dataclasses import dataclass
from typing import Mapping
from typing import Sequence
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy.core.variables.abc import Argument
from rmshared.content.taxonomy.core.variables.abc import Operator
from rmshared.content.taxonomy.core.variables.abc import Reference

Case = TypeVar('Case')


@dataclass(frozen=True)
class Switch(Operator[Case]):
    ref: Reference
    cases: Mapping[Type[Argument], Operator[Case]]


@dataclass(frozen=True)
class Return(Operator[Case]):
    cases: Sequence[Case]
