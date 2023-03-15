from dataclasses import dataclass
from typing import Collection

from rmshared.content.taxonomy.core0.abc import Label
from rmshared.content.taxonomy.core0.abc import Range
from rmshared.content.taxonomy.core0.abc import Filter


@dataclass(frozen=True)
class AnyLabel(Filter):
    labels: Collection[Label]


@dataclass(frozen=True)
class NoLabels(Filter):
    labels: Collection[Label]


@dataclass(frozen=True)
class AnyRange(Filter):
    ranges: Collection[Range]


@dataclass(frozen=True)
class NoRanges(Filter):
    ranges: Collection[Range]
