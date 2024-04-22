from dataclasses import dataclass
from typing import AbstractSet
from typing import Any
from typing import Mapping
from typing import Optional

from rmshared.dataclasses import total_ordering

from rmshared.content.taxonomy import users
from rmshared.content.taxonomy.graph import others


@dataclass(frozen=True)
class UserProfile:
    id: int
    user: 'User'
    slug: str
    title: str
    about_html: str
    description: str
    details: Optional['UserProfileDetails']


@dataclass(frozen=True)
class UserProfileDetails:
    status: users.statuses.Status
    site_specific_info: Mapping[str, Any]
    lifetime_posts_count: int


@dataclass(frozen=True)
class User:
    id: int
    details: Optional['UserDetails']


@dataclass(frozen=True)
class UserDetails:
    status: users.consts.USER.STATUS
    emails: AbstractSet[str]
    groups: AbstractSet['UserGroup']
    communities: AbstractSet[others.Community]
    access_roles: AbstractSet['AccessRole']
    last_login_ts: Optional[int | float]


@dataclass(frozen=True)
@total_ordering
class UserGroup:
    slug: str


@dataclass(frozen=True)
@total_ordering
class AccessRole:
    id: int
