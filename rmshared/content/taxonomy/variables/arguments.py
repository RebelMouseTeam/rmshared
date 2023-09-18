from dataclasses import dataclass
from typing import Sequence
from typing import TypeVar

from rmshared.content.taxonomy.variables.abc import Argument

Scalar = TypeVar('Scalar')


@dataclass(frozen=True)
class Value(Argument[Scalar]):
    values: Sequence[Scalar]


@dataclass(frozen=True)
class Empty(Argument):
    pass


@dataclass(frozen=True)
class Any(Argument):
    pass
