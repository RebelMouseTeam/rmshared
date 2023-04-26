from abc import ABCMeta
from dataclasses import dataclass
from typing import Any

from rmshared.content.taxonomy.abc import Label
from rmshared.content.taxonomy.posts import consts
from rmshared.content.taxonomy.posts import statuses


class Base(Label, metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Id(Base):
    value: int


@dataclass(frozen=True)
class Type(Base):
    type: consts.POST.TYPE


@dataclass(frozen=True)
class Status(Base):
    status: statuses.Status  # TODO: Status(Published), Status(Published(scope=site)), Status(Published(scope=site(...)))


@dataclass(frozen=True)
class Private(Base):
    pass


@dataclass(frozen=True)
class Suspicious(Base):
    pass


@dataclass(frozen=True)
class ExcludedFromSearch(Base):
    pass


@dataclass(frozen=True)
class PrimaryTag(Base):
    slug: str


@dataclass(frozen=True)
class NoPrimaryTags(Base):
    pass


@dataclass(frozen=True)
class RegularTag(Base):
    slug: str


@dataclass(frozen=True)
class NoRegularTags(Base):
    pass


@dataclass(frozen=True)
class PrimarySection(Base):
    id: int


@dataclass(frozen=True)
class NoPrimarySections(Base):
    pass


@dataclass(frozen=True)
class RegularSection(Base):
    id: int


@dataclass(frozen=True)
class NoRegularSections(Base):
    pass


@dataclass(frozen=True)
class Community(Base):
    id: int


@dataclass(frozen=True)
class NoCommunities(Base):
    pass


@dataclass(frozen=True)
class Author(Base):
    id: int


@dataclass(frozen=True)
class NoAuthors(Base):
    pass


@dataclass(frozen=True)
class Stage(Base):
    id: int


@dataclass(frozen=True)
class NoStages(Base):
    pass


@dataclass(frozen=True)
class CustomField(Base):
    path: str
    value: Any


@dataclass(frozen=True)
class NoCustomField(Base):
    path: str


@dataclass(frozen=True)
class DefaultPageLayout(Base):
    pass


@dataclass(frozen=True)
class SpecialPageLayout(Base):
    slug: str


@dataclass(frozen=True)
class DefaultEditorLayout(Base):
    pass


@dataclass(frozen=True)
class SpecialEditorLayout(Base):
    slug: str
