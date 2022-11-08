from typing import AbstractSet
from dataclasses import dataclass

from content.taxonomy.abc import Grouping
from content.taxonomy.abc import Label


@dataclass(frozen=True)
class Labels(Grouping):
    labels: AbstractSet[Label]
