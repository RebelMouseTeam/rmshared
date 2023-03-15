from dataclasses import dataclass

from rmshared.content.taxonomy.core0.abc import Field


@dataclass(frozen=True)
class System(Field):
    name: str


@dataclass(frozen=True)
class Custom(Field):
    name: str
    path: str
