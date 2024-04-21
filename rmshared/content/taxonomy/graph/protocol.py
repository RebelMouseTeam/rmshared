from functools import cached_property
from operator import itemgetter
from typing import Any
from typing import Mapping

from orjson import orjson

from rmshared.typings import read_only

from rmshared.tools import unless_none

from rmshared.content.taxonomy.graph import posts
from rmshared.content.taxonomy.graph import users
from rmshared.content.taxonomy.graph import others
from rmshared.content.taxonomy.graph import sections
from rmshared.content.taxonomy.graph.abc import IProtocol


class Protocol(IProtocol):
    def make_post(self, data):
        from rmshared.tools import merge_dicts
        data = merge_dicts({'embargoed_until_ts': None}, data)  # TODO: remove after migration
        return posts.Post(
            id=int(data['id']),
            type=self.posts.make_post_type(data['type']),
            status=self.posts.make_post_status(data['status']),
            stage_id=unless_none(int)(data['stage_id']),
            is_private=bool(data['is_private']),
            is_suspicious=bool(data['is_suspicious']),
            is_excluded_from_search=bool(data.get('is_excluded_from_search')),
            modified_ts=float(data['modified_ts']),
            scheduled_ts=unless_none(float)(data['scheduled_ts']),
            published_ts=unless_none(float)(data['published_ts']),
            embargoed_until_ts=unless_none(float)(data['embargoed_until_ts']),
            title=str(data['title']),
            subtitles=tuple(map(str, (data['subtitles']))),
            bodies=tuple(map(str, (data['bodies']))),
            primary_tag=unless_none(self._make_tag)(data['primary_tag']),
            regular_tags=frozenset(map(self._make_tag, (data['regular_tags']))),
            primary_section=unless_none(self._make_section)(data['primary_section']),
            regular_sections=frozenset(map(self._make_section, (data['regular_sections']))),
            community=unless_none(self._make_community)(data['community']),
            authors=tuple(map(self.make_user_profile, (data['authors']))),
            page_layout=unless_none(self._make_layout)(data['page_layout']),
            editor_layout=unless_none(self._make_layout)(data['editor_layout']),
            site_specific_info=read_only(dict(data['site_specific_info'])),
            lifetime_page_views_count=int(data['lifetime_page_views_count']),
        )

    def jsonify_post(self, post):
        return {
            'id': post.id,
            'type': self.posts.jsonify_post_type(post.type),
            'status': self.posts.jsonify_post_status(post.status),
            'stage_id': post.stage_id,
            'is_private': post.is_private,
            'is_suspicious': post.is_suspicious,
            'is_excluded_from_search': post.is_excluded_from_search,
            'modified_ts': post.modified_ts,
            'scheduled_ts': post.scheduled_ts,
            'published_ts': post.published_ts,
            'embargoed_until_ts': post.embargoed_until_ts,
            'title': post.title,
            'subtitles': list(post.subtitles),
            'bodies': list(post.bodies),
            'primary_tag': unless_none(self._jsonify_tag)(post.primary_tag),
            'regular_tags': sorted(map(self._jsonify_tag, post.regular_tags), key=itemgetter('slug')),
            'primary_section': unless_none(self._jsonify_section)(post.primary_section),
            'regular_sections': sorted(map(self._jsonify_section, post.regular_sections), key=itemgetter('id')),
            'community': unless_none(self._jsonify_community)(post.community),
            'authors': list(map(self.jsonify_user_profile, post.authors)),
            'page_layout': unless_none(self._jsonify_layout)(post.page_layout),
            'editor_layout': unless_none(self._jsonify_layout)(post.editor_layout),
            'site_specific_info': orjson.loads(orjson.dumps(post.site_specific_info)),
            'lifetime_page_views_count': post.lifetime_page_views_count,
        }

    @staticmethod
    def _make_tag(data: Mapping[str, Any]) -> others.Tag:
        return others.Tag(slug=str(data['slug']))

    @staticmethod
    def _jsonify_tag(tag: others.Tag) -> Mapping[str, Any]:
        return {
            'slug': tag.slug,
        }

    @staticmethod
    def _make_section(data: Mapping[str, Any]) -> sections.Section:
        return sections.Section(id=int(data['id']))

    @staticmethod
    def _jsonify_section(section: sections.Section) -> Mapping[str, Any]:
        return {
            'id': section.id,
        }

    @staticmethod
    def _make_layout(data: Mapping[str, Any]):
        return others.Layout(slug=str(data['slug']))

    @staticmethod
    def _jsonify_layout(layout: others.Layout) -> Mapping[str, Any]:
        return {
            'slug': layout.slug,
        }

    def make_user_profile(self, data):
        return users.UserProfile(
            id=int(data['id']),
            user=self._make_user(data['user']),
            slug=str(data['slug']),
            title=str(data['title']),
            about_html=str(data['about_html']),
            description=str(data['description']),
            details=unless_none(self._make_user_profile_details)(data.get('details')),
        )

    def jsonify_user_profile(self, author: users.UserProfile) -> Mapping[str, Any]:
        return {
            'id': author.id,
            'user': self._jsonify_user(author.user),
            'slug': author.slug,
            'title': author.title,
            'about_html': author.about_html,
            'description': author.description,
            'details': unless_none(self._jsonify_user_profile_details)(author.details),
        }

    def _make_user_profile_details(self, data: Mapping[str, Any]):
        return users.UserProfileDetails(
            status=self.users.make_user_profile_status(data['status']),
            site_specific_info=read_only(dict(data['site_specific_info'])),
            lifetime_posts_count=int(data['lifetime_posts_count']),
        )

    def _jsonify_user_profile_details(self, details: users.UserProfileDetails) -> Mapping[str, Any]:
        return {
            'status': self.users.jsonify_user_profile_status(details.status),
            'site_specific_info': details.site_specific_info,
            'lifetime_posts_count': details.lifetime_posts_count,
        }

    def _make_user(self, data: Mapping[str, Any]):
        return users.User(
            id=int(data['id']),
            details=unless_none(self._make_user_details)(data.get('details')),
        )

    def _jsonify_user(self, user: users.User) -> Mapping[str, Any]:
        return {
            'id': user.id,
            'details': unless_none(self._jsonify_user_details)(user.details),
        }

    def _make_user_details(self, data: Mapping[str, Any]):
        return users.UserDetails(
            status=self.users.make_user_status(data['status']),
            emails=frozenset(map(str, data['emails'])),
            groups=frozenset(map(self._make_user_group, data['groups'])),
            communities=frozenset(map(self._make_community, data['communities'])),
            access_roles=frozenset(map(self._make_access_role, data['access_roles'])),
            last_login_ts=unless_none(float)(data['last_login_ts']),
        )

    def _jsonify_user_details(self, details: users.UserDetails) -> Mapping[str, Any]:
        return {
            'status': self.users.jsonify_user_status(details.status),
            'emails': list(details.emails),
            'groups': list(map(self._jsonify_user_group, details.groups)),
            'communities': list(map(self._jsonify_community, details.communities)),
            'access_roles': list(map(self._jsonify_access_role, details.access_roles)),
            'last_login_ts': details.last_login_ts,
        }

    @staticmethod
    def _make_user_group(data: Mapping[str, Any]):
        return users.UserGroup(slug=str(data['slug']))

    @staticmethod
    def _jsonify_user_group(group: users.UserGroup) -> Mapping[str, Any]:
        return {
            'slug': group.slug,
        }

    @staticmethod
    def _make_access_role(data: Mapping[str, Any]):
        return users.AccessRole(id=int(data['id']))

    @staticmethod
    def _jsonify_access_role(role: users.AccessRole) -> Mapping[str, Any]:
        return {
            'id': role.id,
        }

    def _make_community(self, data: Mapping[str, Any]) -> others.Community:
        return others.Community(
            id=int(data['id']),
            slug=str(data['slug']),
            title=str(data['title']),
            about_html=str(data['about_html']),
            description=str(data['description']),
            details=unless_none(self._make_community_details)(data.get('details')),
        )

    def _jsonify_community(self, community: others.Community) -> Mapping[str, Any]:
        return {
            'id': community.id,
            'slug': community.slug,
            'title': community.title,
            'about_html': community.about_html,
            'description': community.description,
            'details': unless_none(self._jsonify_community_details)(community.details),
        }

    @staticmethod
    def _make_community_details(data: Mapping[str, Any]) -> others.CommunityDetails:
        return others.CommunityDetails(
            site_specific_info=read_only(dict(data['site_specific_info'])),
            lifetime_posts_count=int(data['lifetime_posts_count']),
        )

    @staticmethod
    def _jsonify_community_details(details: others.CommunityDetails) -> Mapping[str, Any]:
        return {
            'site_specific_info': details.site_specific_info,
            'lifetime_posts_count': details.lifetime_posts_count,
        }

    @cached_property
    def posts(self):
        from rmshared.content.taxonomy import posts
        return posts.Protocol()

    @cached_property
    def users(self):
        from rmshared.content.taxonomy import users
        return users.Protocol()
