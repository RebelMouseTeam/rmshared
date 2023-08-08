from dataclasses import dataclass

from rmshared.content.taxonomy import core


@core.aliases.system_field('user-id')
@dataclass(frozen=True)
class Id:
    pass


@core.aliases.system_field('user-profile-slug')
@dataclass(frozen=True)
class Slug:
    pass


@core.aliases.system_field('user-profile-title')
@dataclass(frozen=True)
class Title:
    pass


@core.aliases.system_field('user-profile-owner')
@dataclass(frozen=True)
class Owner:
    pass


@core.aliases.system_field('user-profile-status')
@dataclass(frozen=True)
class Status:
    pass


@core.aliases.system_field('user-email')
@dataclass(frozen=True)
class Email:
    pass


@core.aliases.system_field('user-group')
@dataclass(frozen=True)
class Group:
    pass


@core.aliases.system_field('user-community')
@dataclass(frozen=True)
class Community:
    pass


@core.aliases.system_field('user-access-role')
@dataclass(frozen=True)
class AccessRole:
    pass


@core.aliases.system_field('user-last-logged-in-at')
@dataclass(frozen=True)
class LastLoggedInAt:
    pass


@core.aliases.custom_field('user-custom-field')
@dataclass(frozen=True)
class CustomField:
    path: str
