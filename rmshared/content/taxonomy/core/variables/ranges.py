from dataclasses import dataclass

from rmshared.content.taxonomy.core import ranges as core_ranges
from rmshared.content.taxonomy.core.abc import Range

from rmshared.content.taxonomy.core.variables.abc import Cases
from rmshared.content.taxonomy.core.variables.abc import Constant
from rmshared.content.taxonomy.core.variables.abc import Reference
from rmshared.content.taxonomy.core.variables.abc import Variable


@dataclass(frozen=True)
class Switch(Range):
    ref: Reference
    cases: Cases


@dataclass(frozen=True)
class Between(core_ranges.Between):
    min_value: Variable | Constant
    max_value: Variable | Constant


@dataclass(frozen=True)
class LessThan(core_ranges.LessThan):
    value: Variable


@dataclass(frozen=True)
class MoreThan(core_ranges.MoreThan):
    value: Variable
