from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Sequence

from rmshared.content.taxonomy import sections
from rmshared.content.taxonomy.graph import others


@dataclass(frozen=True)
class Section:
    id: int
    details: Optional[SectionDetails]


@dataclass(frozen=True)
class SectionDetails:
    path: str
    slug: str
    title: str
    order_id: int
    created_ts: int
    is_read_only: bool
    ancestors: Sequence[Section]
    visibility: sections.consts.VISIBILITY.STATUS
    access: SectionAccess
    settings: SectionSettings
    meta_info: SectionMetaInfo
    site_specific_info: Mapping[str, Any]


@dataclass(frozen=True)
class SectionAccess:
    read_access_kind: sections.access.Kind


@dataclass(frozen=True)
class SectionSettings:
    open_in_new_tab: bool
    allow_community_posts: bool
    hide_from_entry_editor: bool
    lock_posts_after_publishing: bool


@dataclass(frozen=True)
class SectionMetaInfo:
    image: Optional[others.Image]
    link_out: Optional[str]
    meta_tags: Sequence[str]
    meta_title: str
    about_html: str
