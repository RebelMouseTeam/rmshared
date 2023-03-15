from dataclasses import dataclass

from rmshared.content.taxonomy.core0.abc import Order
from rmshared.content.taxonomy.core0.abc import Field


@dataclass(frozen=True)
class Value(Order):
    field: Field
    reverse: bool
