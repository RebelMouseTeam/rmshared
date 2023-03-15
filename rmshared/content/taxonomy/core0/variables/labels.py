from dataclasses import dataclass

from rmshared.content.taxonomy.core0 import labels as scalar_labels
from rmshared.content.taxonomy.core0.abc import Label
from rmshared.content.taxonomy.core0.variables.abc import Cases
from rmshared.content.taxonomy.core0.variables.abc import Reference
from rmshared.content.taxonomy.core0.variables.abc import Variable


@dataclass(frozen=True)
class Switch(Label):
    ref: Reference
    cases: Cases


@dataclass(frozen=True)
class Value(scalar_labels.Value):
    value: Variable
