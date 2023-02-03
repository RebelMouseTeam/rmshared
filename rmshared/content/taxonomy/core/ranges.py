from dataclasses import dataclass

from rmshared.content.taxonomy.core.abc import Field
from rmshared.content.taxonomy.core.abc import Range
from rmshared.content.taxonomy.core.abc import Scalar


@dataclass(frozen=True)
class Between(Range):
    field: Field
    min_value: Scalar
    max_value: Scalar


@dataclass(frozen=True)
class LessThan(Range):
    field: Field
    value: Scalar


@dataclass(frozen=True)
class MoreThan(Range):
    field: Field
    value: Scalar
