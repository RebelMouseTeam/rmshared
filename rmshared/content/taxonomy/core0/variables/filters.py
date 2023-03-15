from dataclasses import dataclass

from rmshared.content.taxonomy.core0.abc import Filter
from rmshared.content.taxonomy.core0.variables.abc import Cases
from rmshared.content.taxonomy.core0.variables.abc import Reference


@dataclass(frozen=True)
class Switch(Filter):
    ref: Reference
    cases: Cases
