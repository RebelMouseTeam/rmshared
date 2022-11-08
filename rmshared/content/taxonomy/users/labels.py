from dataclasses import dataclass
from typing import Any

from rmshared.content.taxonomy.abc import Label
from rmshared.content.taxonomy.users import statuses


@dataclass(frozen=True)
class Id(Label):
    value: int


@dataclass(frozen=True)
class Owner(Label):
    user_id: int


@dataclass(frozen=True)
class Status(Label):
    status: statuses.Status


@dataclass(frozen=True)
class UserGroup(Label):
    slug: str


@dataclass(frozen=True)
class NoUserGroups(Label):
    pass


@dataclass(frozen=True)
class Community(Label):
    id: int


@dataclass(frozen=True)
class NoCommunities(Label):
    pass


@dataclass(frozen=True)
class AccessRole(Label):
    id: int


@dataclass(frozen=True)
class NoAccessRoles(Label):
    pass


@dataclass(frozen=True)
class CustomField(Label):
    path: str
    value: Any


@dataclass(frozen=True)
class NoCustomField(Label):
    path: str
