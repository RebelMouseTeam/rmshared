from dataclasses import dataclass

from rmshared.content.taxonomy.core0 import ranges as core0_ranges
from rmshared.content.taxonomy.core0.abc import Range

from rmshared.content.taxonomy.core0.variables.abc import Cases
from rmshared.content.taxonomy.core0.variables.abc import Constant
from rmshared.content.taxonomy.core0.variables.abc import Reference
from rmshared.content.taxonomy.core0.variables.abc import Variable


@dataclass(frozen=True)
class Switch(Range):
    ref: Reference
    cases: Cases


@dataclass(frozen=True)
class Between(core0_ranges.Between):
    min_value: Variable | Constant
    max_value: Variable | Constant


@dataclass(frozen=True)
class LessThan(core0_ranges.LessThan):
    value: Variable


@dataclass(frozen=True)
class MoreThan(core0_ranges.MoreThan):
    value: Variable
