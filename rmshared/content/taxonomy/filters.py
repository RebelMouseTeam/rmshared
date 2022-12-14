from typing import Any
from typing import Mapping
from typing import Optional
from typing import Sequence
from dataclasses import dataclass

from rmshared.content.taxonomy.abc import Filter
from rmshared.content.taxonomy.abc import Label
from rmshared.content.taxonomy.abc import Range


@dataclass(frozen=True)
class Phrase(Filter):
    phrase: str
    syntax: Optional[Mapping[str, Any]]
    weights: Optional[Sequence[int]]  # TODO: should we move it to `orders.Relevance`? Probably, we should (@see `matcher.Matcher`). Or need to modify it


@dataclass(frozen=True)
class AnyRange(Filter):
    ranges: Sequence[Range]


@dataclass(frozen=True)
class NoRanges(Filter):
    ranges: Sequence[Range]


@dataclass(frozen=True)
class AnyLabel(Filter):
    labels: Sequence[Label]


@dataclass(frozen=True)
class NoLabels(Filter):
    labels: Sequence[Label]
