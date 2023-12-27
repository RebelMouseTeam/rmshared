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
    post_aspects = posts.Aspects()
    user_aspects = users.Aspects()

    @classmethod
    def make_values_extractor_for_post(cls, post: graph.posts.Post) -> IValuesExtractor:
        field_name_to_system_values_streamer_map: Mapping[str, Callable[[], Iterable[Scalar]]] = {
            posts.fields.Id.name: lambda: [post.id],
            posts.fields.Type.name: lambda: map(cls.post_aspects.map_post_type, [post.type]),
            posts.fields.Status.name: lambda: map(cls.post_aspects.map_post_status, [post.status]),
            posts.fields.IsPrivate.name: lambda: [post.is_private],
            posts.fields.IsSuspicious.name: lambda: [post.is_suspicious],
            posts.fields.IsExcludedFromSearch.name: lambda: [post.is_excluded_from_search],
            posts.fields.ModifiedAt.name: lambda: [post.modified_ts],
            posts.fields.ScheduledAt.name: lambda: filter(None, [post.scheduled_ts]),
            posts.fields.PublishedAt.name: lambda: filter(None, [post.published_ts]),
            posts.fields.EmbargoedUntil.name: lambda: filter(None, [post.embargoed_until_ts]),
            posts.fields.Title.name: lambda: [post.title],
            posts.fields.Subtitle.name: lambda: post.subtitles,
            posts.fields.Body.name: lambda: post.bodies,
            posts.fields.PrimaryTag.name: lambda: map(attrgetter('slug'), filter(None, [post.primary_tag])),
            posts.fields.RegularTag.name: lambda: sorted(map(attrgetter('slug'), post.regular_tags)),
            posts.fields.PrimarySection.name: lambda: map(attrgetter('id'), filter(None, [post.primary_section])),
            posts.fields.RegularSection.name: lambda: sorted(map(attrgetter('id'), post.regular_sections)),
            posts.fields.Community.name: lambda: map(attrgetter('id'), filter(None, [post.community])),
            posts.fields.Author.name: lambda: map(attrgetter('id'), post.authors),
            posts.fields.Stage.name: lambda: filter(None, [post.stage_id]),
            posts.fields.PageLayout.name: lambda: map(attrgetter('slug'), filter(None, [post.page_layout])),
            posts.fields.EditorLayout.name: lambda: map(attrgetter('slug'), filter(None, [post.editor_layout])),
            posts.fields.PageViewsCount.name: lambda: [post.lifetime_page_views_count],
        }
        field_name_to_custom_values_getter_map: Mapping[str, Callable[[], Mapping[str, Any]]] = {
            posts.fields.CustomField.name: lambda: post.site_specific_info,
        }
        return ValuesExtractor(field_name_to_system_values_streamer_map, field_name_to_custom_values_getter_map)

    @classmethod
    def make_values_extractor_for_user_profile(cls, user_profile: graph.users.UserProfile) -> IValuesExtractor:
        field_name_to_system_values_streamer_map: Mapping[str, Callable[[], Iterable[Scalar]]] = {
            users.fields.Id.name: lambda: [user_profile.id],
            users.fields.Email.name: lambda: user_profile.user.details.emails,
            users.fields.Slug.name: lambda: [user_profile.slug],
            users.fields.Title.name: lambda: [user_profile.title],
            users.fields.Owner.name: lambda: [user_profile.user.id],
            users.fields.Status.name: lambda: map(cls.user_aspects.map_user_profile_status, [user_profile.details.status]),
            users.fields.AboutHtml.name: lambda: [user_profile.about_html],
            users.fields.Description.name: lambda: [user_profile.description],
            users.fields.Group.name: lambda: map(attrgetter('slug'), user_profile.user.details.groups),
            users.fields.Community.name: lambda: map(attrgetter('id'), user_profile.user.details.communities),
            users.fields.AccessRole.name: lambda: map(attrgetter('id'), user_profile.user.details.access_roles),
            users.fields.LastLoggedInAt.name: lambda: filter(None, [user_profile.user.details.last_login_ts]),
            users.fields.PostsCount.name: lambda: [user_profile.details.lifetime_posts_count],
        }
        field_name_to_custom_values_getter_map: Mapping[str, Callable[[], Mapping[str, Any]]] = {
            users.fields.CustomField.name: lambda: user_profile.details.site_specific_info,
        }
        return ValuesExtractor(field_name_to_system_values_streamer_map, field_name_to_custom_values_getter_map)
