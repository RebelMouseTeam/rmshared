from __future__ import annotations

from abc import ABCMeta
from dataclasses import dataclass
from typing import Type

from rmshared.content.taxonomy.abc import Guid


@dataclass(frozen=True)
class Scope(metaclass=ABCMeta):
    ...


@dataclass(frozen=True)
class Entity(Scope):
    entity: Type[Guid]
