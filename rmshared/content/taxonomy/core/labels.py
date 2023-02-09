from dataclasses import dataclass

from rmshared.content.taxonomy.core.abc import Field
from rmshared.content.taxonomy.core.abc import Label
from rmshared.content.taxonomy.core.abc import Scalar


@dataclass(frozen=True)
class Value(Label):
    field: Field
    value: Scalar


@dataclass(frozen=True)
class Badge(Label):
    field: Field


@dataclass(frozen=True)
class Empty(Label):
    field: Field
