from dataclasses import dataclass
from typing import Any

from content.taxonomy.abc import Label
from content.taxonomy.posts import consts
from content.taxonomy.posts import statuses


@dataclass(frozen=True)
class Id(Label):
    value: int


@dataclass(frozen=True)
class Type(Label):
    type: consts.POST.TYPE


@dataclass(frozen=True)
class Status(Label):
    status: statuses.Status


@dataclass(frozen=True)
class Private(Label):
    pass


@dataclass(frozen=True)
class Suspicious(Label):
    pass


@dataclass(frozen=True)
class PrimaryTag(Label):
    slug: str


@dataclass(frozen=True)
class NoPrimaryTags(Label):
    pass


@dataclass(frozen=True)
class RegularTag(Label):
    slug: str


@dataclass(frozen=True)
class NoRegularTags(Label):
    pass


@dataclass(frozen=True)
class PrimarySection(Label):
    id: int


@dataclass(frozen=True)
class NoPrimarySections(Label):
    pass


@dataclass(frozen=True)
class RegularSection(Label):
    id: int


@dataclass(frozen=True)
class NoRegularSections(Label):
    pass


@dataclass(frozen=True)
class Community(Label):
    id: int


@dataclass(frozen=True)
class NoCommunities(Label):
    pass


@dataclass(frozen=True)
class Author(Label):
    id: int


@dataclass(frozen=True)
class NoAuthors(Label):
    pass


@dataclass(frozen=True)
class Stage(Label):
    id: int


@dataclass(frozen=True)
class NoStages(Label):
    pass


@dataclass(frozen=True)
class CustomField(Label):
    path: str
    value: Any


@dataclass(frozen=True)
class NoCustomField(Label):
    path: str


@dataclass(frozen=True)
class DefaultPageLayout(Label):
    pass


@dataclass(frozen=True)
class SpecialPageLayout(Label):
    slug: str


@dataclass(frozen=True)
class DefaultEditorLayout(Label):
    pass


@dataclass(frozen=True)
class SpecialEditorLayout(Label):
    slug: str
