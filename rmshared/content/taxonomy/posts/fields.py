from abc import ABCMeta
from dataclasses import dataclass

from rmshared.content.taxonomy.abc import Field


class Base(Field, metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class PrimaryTag(Base):
    pass


@dataclass(frozen=True)
class RegularTag(Base):
    pass


@dataclass(frozen=True)
class PrimarySection(Base):
    pass


@dataclass(frozen=True)
class RegularSection(Base):
    pass


@dataclass(frozen=True)
class ModifiedAt(Base):
    pass


@dataclass(frozen=True)
class ScheduledAt(Base):
    pass


@dataclass(frozen=True)
class PublishedAt(Base):
    pass


@dataclass(frozen=True)
class LifetimePageViews(Base):  # TODO: == Metric(event='lifetime_page_views') ???
    pass


@dataclass(frozen=True)
class Metric(Base):
    event: str


@dataclass(frozen=True)
class CustomField(Base):
    path: str
