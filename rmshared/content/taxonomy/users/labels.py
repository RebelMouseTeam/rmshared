from abc import ABCMeta
from dataclasses import dataclass
from typing import Any

from rmshared.content.taxonomy.users import statuses


class Base(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Id(Base):
    value: int


@dataclass(frozen=True)
class Slug(Base):
    slug: str


@dataclass(frozen=True)
class Title(Base):
    title: str


@dataclass(frozen=True)
class Email(Base):
    email: str


@dataclass(frozen=True)
class NoEmails(Base):
    pass


@dataclass(frozen=True)
class Owner(Base):
    user_id: int


@dataclass(frozen=True)
class Status(Base):
    status: statuses.Status


@dataclass(frozen=True)
class UserGroup(Base):
    slug: str


@dataclass(frozen=True)
class NoUserGroups(Base):
    pass


@dataclass(frozen=True)
class Community(Base):
    id: int


@dataclass(frozen=True)
class NoCommunities(Base):
    pass


@dataclass(frozen=True)
class AccessRole(Base):
    id: int


@dataclass(frozen=True)
class NoAccessRoles(Base):
    pass


@dataclass(frozen=True)
class CustomField(Base):
    path: str
    value: Any


@dataclass(frozen=True)
class NoCustomField(Base):
    path: str
