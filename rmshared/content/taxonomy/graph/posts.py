from dataclasses import dataclass
from typing import Any
from typing import Mapping
from typing import AbstractSet
from typing import Sequence
from typing import Optional

from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy.graph import others
from rmshared.content.taxonomy.graph import users


@dataclass(frozen=True)
class Post:
    id: int
    type: posts.consts.POST.TYPE
    status: posts.statuses.Status
    stage_id: Optional[int]
    is_private: bool
    is_suspicious: bool
    is_excluded_from_search: bool
    modified_ts: int
    scheduled_ts: Optional[int]
    published_ts: Optional[int]
    title: str
    subtitles: Sequence[str]
    bodies: Sequence[str]
    primary_tag: Optional[others.Tag]
    regular_tags: AbstractSet[others.Tag]
    primary_section: Optional[others.Section]
    regular_sections: AbstractSet[others.Section]
    community: Optional[others.Community]
    authors: Sequence[users.UserProfile]
    page_layout: Optional[others.Layout]
    editor_layout: Optional[others.Layout]
    site_specific_info: Mapping[str, Any]
