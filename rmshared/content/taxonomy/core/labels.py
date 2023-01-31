from dataclasses import dataclass
from typing import Any

from rmshared.content.taxonomy.abc import Label
from rmshared.content.taxonomy.core.abc import Prop


@dataclass(frozen=True)
class HasProp(Label):
    prop: Prop
    value: Any


@dataclass(frozen=True)
class HasNoProp(Label):
    prop: Prop
