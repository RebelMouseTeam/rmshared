from dataclasses import dataclass
from typing import Any
from typing import Mapping
from typing import Optional


@dataclass(frozen=True)
class Tag:
    slug: str


@dataclass(frozen=True)
class Section:
    id: int


@dataclass(frozen=True)
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
