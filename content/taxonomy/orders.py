from dataclasses import dataclass
from typing import Optional

from content.taxonomy.abc import Order
from content.taxonomy.abc import Field


@dataclass(frozen=True)
class Value(Order):
    field: Field
    reverse: bool


@dataclass(frozen=True)
class Relevance(Order):
    decay: Optional['Decay']


@dataclass(frozen=True)
class Decay:
    field: Field
    speed: float
