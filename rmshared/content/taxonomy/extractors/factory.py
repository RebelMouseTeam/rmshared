from operator import attrgetter
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Mapping

from rmshared.content.taxonomy import graph
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import users

from rmshared.content.taxonomy.extractors.abc import Scalar
from rmshared.content.taxonomy.extractors.abc import IValuesExtractor
from rmshared.content.taxonomy.extractors.values import ValuesExtractor


class Factory:
    post_aspects = posts.mappers.Aspects()
    user_aspects = users.mappers.Aspects()

    @classmethod
    def make_values_extractor_for_post(cls, post: graph.posts.Post) -> IValuesExtractor:
        field_name_to_system_values_streamer_map: Mapping[str, Callable[[], Iterable[Scalar]]] = {
            'post-id': lambda: [post.id],
            'post-type': lambda: map(cls.post_aspects.map_post_type, [post.type]),
            'post-status': lambda: map(cls.post_aspects.map_post_status, [post.status]),
            'post-is-private': lambda: [post.is_private],
            'post-is-suspicious': lambda: [post.is_suspicious],
            'post-is-excluded-from-search': lambda: [post.is_excluded_from_search],
            'post-modified-at': lambda: [post.modified_ts],
            'post-scheduled-at': lambda: filter(None, [post.scheduled_ts]),
            'post-published-at': lambda: filter(None, [post.published_ts]),
            'post-title': lambda: [post.title],
            'post-subtitle': lambda: post.subtitles,
            'post-body': lambda: post.bodies,
            'post-primary-tag': lambda: map(attrgetter('slug'), filter(None, [post.primary_tag])),
            'post-regular-tag': lambda: sorted(map(attrgetter('slug'), post.regular_tags)),
            'post-primary-section': lambda: map(attrgetter('id'), filter(None, [post.primary_section])),
            'post-regular-section': lambda: sorted(map(attrgetter('id'), post.regular_sections)),
            'post-community': lambda: map(attrgetter('id'), filter(None, [post.community])),
            'post-author': lambda: map(attrgetter('id'), post.authors),
            'post-stage': lambda: filter(None, [post.stage_id]),
            'post-page-layout': lambda: map(attrgetter('slug'), filter(None, [post.page_layout])),
            'post-editor-layout': lambda: map(attrgetter('slug'), filter(None, [post.editor_layout])),
            'post-page-views-count': lambda: [post.lifetime_page_views_count],
        }
        field_name_to_custom_values_getter_map: Mapping[str, Callable[[], Mapping[str, Any]]] = {
            'post-custom-field': lambda: post.site_specific_info,
        }
        return ValuesExtractor(field_name_to_system_values_streamer_map, field_name_to_custom_values_getter_map)

    @classmethod
    def make_values_extractor_for_user_profile(cls, user_profile: graph.users.UserProfile) -> IValuesExtractor:
        field_name_to_system_values_streamer_map: Mapping[str, Callable[[], Iterable[Scalar]]] = {
            'user-id': lambda: [user_profile.id],
            'user-email': lambda: user_profile.user.details.emails,
            'user-profile-slug': lambda: [user_profile.slug],
            'user-profile-title': lambda: [user_profile.title],
            'user-profile-owner': lambda: [user_profile.user.id],
            'user-profile-status': lambda: map(cls.user_aspects.map_user_profile_status, [user_profile.details.status]),
            'user-profile-about-html': lambda: [user_profile.about_html],
            'user-profile-description': lambda: [user_profile.description],
            'user-group': lambda: map(attrgetter('slug'), user_profile.user.details.groups),
            'user-community': lambda: map(attrgetter('id'), user_profile.user.details.communities),
            'user-access-role': lambda: map(attrgetter('id'), user_profile.user.details.access_roles),
            'user-last-logged-in-at': lambda: filter(None, [user_profile.user.details.last_login_ts]),
            'user-posts-count': lambda: [user_profile.details.lifetime_posts_count],
        }
        field_name_to_custom_values_getter_map: Mapping[str, Callable[[], Mapping[str, Any]]] = {
            'user-custom-field': lambda: user_profile.details.site_specific_info,
        }
        return ValuesExtractor(field_name_to_system_values_streamer_map, field_name_to_custom_values_getter_map)
