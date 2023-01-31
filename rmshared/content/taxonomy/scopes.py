from dataclasses import dataclass
from typing import AbstractSet

from rmshared.typings import T
from rmshared.content.taxonomy.abc import Filter
from rmshared.content.taxonomy.abc import Scope


@dataclass(frozen=True)
class Values(Scope[T]):
    values: AbstractSet[T]


@dataclass(frozen=True)
class Sections(Scope[int]):
    filters: AbstractSet[Filter]


@dataclass(frozen=True)
class PostPrimaryTags(Scope[str]):
    pass


@dataclass(frozen=True)
class PostRegularTags(Scope[str]):
    pass


@dataclass(frozen=True)
class PostPrimarySections(Scope[int]):
    pass


@dataclass(frozen=True)
class PostRegularSections(Scope[int]):
    pass
