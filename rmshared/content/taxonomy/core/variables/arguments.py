from dataclasses import dataclass
from typing import Sequence

from rmshared.content.taxonomy.core.abc import Scalar
from rmshared.content.taxonomy.core.variables.abc import Argument


@dataclass(frozen=True)
class Value(Argument):
    values: Sequence[Scalar]


@dataclass(frozen=True)
class Empty(Argument):
    pass


@dataclass(frozen=True)
class Any(Argument):
    pass
