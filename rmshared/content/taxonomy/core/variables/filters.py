from dataclasses import dataclass

from rmshared.content.taxonomy.core.abc import Filter
from rmshared.content.taxonomy.core.variables.abc import Cases
from rmshared.content.taxonomy.core.variables.abc import Reference


@dataclass(frozen=True)
class Switch(Filter):
    ref: Reference
    cases: Cases
