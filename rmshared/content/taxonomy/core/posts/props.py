from dataclasses import dataclass
from typing import Optional

from rmshared.content.taxonomy.core.abc import Prop
from rmshared.content.taxonomy.abc import Scalar

from rmshared.content.taxonomy.posts import consts
from rmshared.content.taxonomy.posts import statuses


@dataclass(frozen=True)
class Id(Prop[int]):
    pass


@dataclass(frozen=True)
class Type(Prop[consts.POST.TYPE]):
    pass


@dataclass(frozen=True)
class Status(Prop[statuses.Status]):
    pass


@dataclass(frozen=True)
class IsPrivate(Prop[bool]):
    pass


@dataclass(frozen=True)
class IsSuspicious(Prop[bool]):
    pass


@dataclass(frozen=True)
class PrimaryTag(Prop[str]):
    pass


@dataclass(frozen=True)
class RegularTag(Prop[str]):
    pass


@dataclass(frozen=True)
class PrimarySection(Prop[int]):
    pass


@dataclass(frozen=True)
class RegularSection(Prop[int]):
    pass


@dataclass(frozen=True)
class Community(Prop[int]):
    pass


@dataclass(frozen=True)
class Author(Prop[int]):
    pass


@dataclass(frozen=True)
class Stage(Prop[int]):
    pass


@dataclass(frozen=True)
class PageLayout(Prop[Optional[str]]):
    pass


@dataclass(frozen=True)
class EditorLayout(Prop[Optional[str]]):
    pass


@dataclass(frozen=True)
class ModifiedAt(Prop[int]):
    pass


@dataclass(frozen=True)
class ScheduledAt(Prop[int]):
    pass


@dataclass(frozen=True)
class PublishedAt(Prop[int]):
    pass


@dataclass(frozen=True)
class LifetimePageViews(Prop[int]):  # TODO: == Metric(event='lifetime_page_views') ???
    pass


@dataclass(frozen=True)
class Metric(Prop[Scalar]):
    event: str


@dataclass(frozen=True)
class CustomField(Prop[Scalar]):
    path: str


"""
class HasLabel(Generic[T]):
    prop: 'Prop[T]'
    value: T


class HasNotLabel(Generic[T]):
    prop: 'Prop[T]'


class Value(Generic[T]):
    prop: 'Prop[T]'
    value: T
"""
