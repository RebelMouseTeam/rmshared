from typing import AbstractSet
from dataclasses import dataclass

from rmshared.content.taxonomy.abc import Grouping
from rmshared.content.taxonomy.abc import Label


@dataclass(frozen=True)
class Labels(Grouping):
    labels: AbstractSet[Label]
