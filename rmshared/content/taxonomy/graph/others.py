from dataclasses import dataclass
from typing import Any
from typing import Mapping
from typing import Optional

from rmshared.dataclasses import total_ordering


@dataclass(frozen=True)
@total_ordering
class Tag:
    slug: str


@dataclass(frozen=True)
@total_ordering
class Community:
    id: int
    slug: str
    title: str
    about_html: str
    description: str
    details: Optional['CommunityDetails']


@dataclass(frozen=True)
class CommunityDetails:
    site_specific_info: Mapping[str, Any]
    lifetime_posts_count: int


@dataclass(frozen=True)
class Layout:
    slug: str


@dataclass(frozen=True)
class Image:
    id: int
