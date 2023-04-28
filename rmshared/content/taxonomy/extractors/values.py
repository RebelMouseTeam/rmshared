from operator import attrgetter
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import ItemGetter

from rmshared.content.taxonomy import graph
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.extractors.abc import IValuesExtractor

Field = TypeVar('Field', bound=core.fields.Field)


class PostValuesExtractor(IValuesExtractor):
    mapper = posts.mappers.Aspects()  # TODO: do something!

    def __init__(self, post: graph.posts.Post):
        self.post = post
        self.core_field_to_values_extractor_map: Mapping[Type[core.fields.Field], Callable[[Field], Iterable[str | int | float | bool]]] = {
            core.fields.System: self._extract_system_field_values,
            core.fields.Custom: self._extract_custom_field_values,
        }
        self.core_field_name_to_values_extractor_map: Mapping[str, Callable[[], Iterable[str | int | float | bool]]] = {  # TODO: connect to `posts.mappers`
            'post-id': lambda: [self.post.id],
            'post-type': lambda: map(self.mapper.map_post_type, [self.post.type]),
            'post-status': lambda: map(self.mapper.map_post_status, [self.post.status]),
            'post-stage': lambda: filter(None, [self.post.stage_id]),
            'post-is-private': lambda: [self.post.is_private],
            'post-is-suspicious': lambda: [self.post.is_suspicious],
            'post-is-excluded-from-search': lambda: [self.post.is_excluded_from_search],
            'post-modified-at': lambda: [self.post.modified_ts],
            'post-scheduled-at': lambda: filter(None, [self.post.scheduled_ts]),
            'post-published-at': lambda: filter(None, [self.post.published_ts]),
            'post-title': lambda: [self.post.title],
            'post-subtitle': lambda: self.post.subtitles,
            'post-body': lambda: self.post.bodies,
            'post-primary-tag': lambda: map(attrgetter('slug'), filter(None, [self.post.primary_tag])),
            'post-regular-tag': lambda: sorted(map(attrgetter('slug'), self.post.regular_tags)),
            'post-primary-section': lambda: map(attrgetter('id'), filter(None, [self.post.primary_section])),
            'post-regular-section': lambda: sorted(map(attrgetter('id'), self.post.regular_sections)),
            'post-community': lambda: map(attrgetter('id'), filter(None, [self.post.community])),
            'post-author': lambda: map(attrgetter('id'), self.post.authors),
            'post-page-layout': lambda: map(attrgetter('slug'), filter(None, [self.post.page_layout])),
            'post-editor-layout': lambda: map(attrgetter('slug'), filter(None, [self.post.editor_layout])),
        }
        self.core_field_name_to_custom_values_getter_map: Mapping[str, Callable[[], Mapping[str, Any]]] = {
            'post-site-specific-info': lambda: self.post.site_specific_info,
        }

    def extract_values(self, field):
        return iter(self.core_field_to_values_extractor_map[type(field)](field))

    def _extract_system_field_values(self, field: core.fields.System) -> Iterable[str | int | float | bool]:
        return self.core_field_name_to_values_extractor_map[field.name]()

    def _extract_custom_field_values(self, field: core.fields.Custom) -> Iterable[str | int | float | bool]:
        try:
            item = ItemGetter(field.path)(self.core_field_name_to_custom_values_getter_map[field.name]())
        except LookupError:
            return []

        if isinstance(item, str):
            return [item]
        elif isinstance(item, Iterable):
            return filter(None, item)
        else:
            return filter(None, [item])
