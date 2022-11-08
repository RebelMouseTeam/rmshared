from dataclasses import dataclass

from content.taxonomy.abc import Field


@dataclass(frozen=True)
class Title(Field):
    pass


@dataclass(frozen=True)
class LastLoggedInAt(Field):
    pass


@dataclass(frozen=True)
class LifetimePosts(Field):
    pass


@dataclass(frozen=True)
class CustomField(Field):
    path: str
