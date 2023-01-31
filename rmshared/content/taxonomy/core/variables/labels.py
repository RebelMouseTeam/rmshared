from dataclasses import dataclass

from rmshared.content.taxonomy.core import labels as scalar_labels
from rmshared.content.taxonomy.core.abc import Label
from rmshared.content.taxonomy.core.variables.abc import Cases
from rmshared.content.taxonomy.core.variables.abc import Reference
from rmshared.content.taxonomy.core.variables.abc import Variable


@dataclass(frozen=True)
class Switch(Label):
    ref: Reference
    cases: Cases


@dataclass(frozen=True)
class Value(scalar_labels.Value):
    value: Variable
