from abc import ABCMeta
from dataclasses import dataclass


class Base(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Author(Base):
    pass


@dataclass(frozen=True)
class Community(Base):
    pass


@dataclass(frozen=True)
class PrimaryTag(Base):  # TODO: taxonomy.aliases.posts.fields.PrimaryTag ???
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
class CustomField(Base):
    path: str
