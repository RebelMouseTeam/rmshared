from dataclasses import dataclass

from rmshared.content.taxonomy.variables.abc import Variable


@dataclass(frozen=True)
class Sections(Variable):
    ids: None