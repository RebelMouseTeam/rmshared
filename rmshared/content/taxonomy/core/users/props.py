from dataclasses import dataclass

from rmshared.content.taxonomy.core.abc import Prop

from rmshared.content.taxonomy.abc import Scalar
from rmshared.content.taxonomy.users import statuses


@dataclass(frozen=True)
class Id(Prop[int]):
    pass


@dataclass(frozen=True)
class Owner(Prop[int]):
    pass


@dataclass(frozen=True)
class Status(Prop[statuses.Status]):
    pass


@dataclass(frozen=True)
class UserGroup(Prop[str]):
    pass


@dataclass(frozen=True)
class Community(Prop[int]):
    pass


@dataclass(frozen=True)
class AccessRole(Prop[int]):
    pass


@dataclass(frozen=True)
class Title(Prop[str]):
    pass


@dataclass(frozen=True)
class LastLoggedInAt(Prop[int]):
    pass


@dataclass(frozen=True)
class LifetimePosts(Prop[int]):
    pass


@dataclass(frozen=True)
class CustomProp(Prop[Scalar]):
    path: str
