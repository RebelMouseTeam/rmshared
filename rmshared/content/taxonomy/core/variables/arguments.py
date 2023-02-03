from dataclasses import dataclass

from rmshared.content.taxonomy.core.variables.abc import Argument


@dataclass(frozen=True)
class Value(Argument):
    pass


@dataclass(frozen=True)
class Empty(Argument):
    pass


@dataclass(frozen=True)
class Any(Argument):
    pass
