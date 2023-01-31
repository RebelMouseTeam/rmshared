from dataclasses import dataclass
from typing import Collection
from typing import Generic
from typing import Optional
from typing import TypeVar

from rmshared.content.taxonomy.core.abc import Label
from rmshared.content.taxonomy.core.abc import Range
from rmshared.content.taxonomy.core.abc import Filter

Payload = TypeVar('Payload')


@dataclass(frozen=True)
class Phrase(Generic[Payload], Filter):  # TODO: Move out from `rmshared`?
    phrase: str
    payload: Optional[Payload]


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
