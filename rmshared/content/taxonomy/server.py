from typing import AbstractSet
from typing import Any
from typing import Iterable
from typing import Iterator
from typing import Mapping

from rmshared.tools import apply
from rmshared.tools import ensure_map_is_complete
from rmshared.tools import invert_dict
from rmshared.tools import parse_name_and_info
from rmshared.tools import unless_none
from rmshared.typings import read_only

from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import users
from rmshared.content.taxonomy import orders
from rmshared.content.taxonomy import filters
from rmshared.content.taxonomy.abc import Text
from rmshared.content.taxonomy.abc import Label
from rmshared.content.taxonomy.abc import Field
from rmshared.content.taxonomy.abc import Range
from rmshared.content.taxonomy.abc import Condition
from rmshared.content.taxonomy.abc import Filter
from rmshared.content.taxonomy.abc import Order


class Protocol:
    def __init__(self):
        self.posts = self.Posts(self)
        self.users = self.Users(self)
        self.texts = self.Texts(self)
        self.labels = self.Labels(self)
        self.fields = self.Fields(self)
        self.orders = self.Orders(self)
        self.filters = self.Filters(self)
        self.conditions = self.Conditions()

    class Posts:
        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.post_status_to_factory_func_map = ensure_map_is_complete(posts.statuses.Status, {
                posts.statuses.Draft: self._make_draft_post_status,
                posts.statuses.Published: self._make_published_post_status,
                posts.statuses.Removed: lambda _: posts.statuses.Removed(),
            })
            self.draft_post_stage_to_factory_func_map = ensure_map_is_complete(posts.drafts.stages.Stage, {
                posts.drafts.stages.Created: self._make_draft_post_created_stage,
                posts.drafts.stages.InProgress: self._make_draft_post_in_progress_stage,
                posts.drafts.stages.InReview: lambda _: posts.drafts.stages.InReview(),
                posts.drafts.stages.Ready: lambda _: posts.drafts.stages.Ready(),
            })
            self.published_post_scope_to_factory_func_map = ensure_map_is_complete(posts.published.scopes.Scope, {
                posts.published.scopes.Site: self._make_published_post_site_scope,
                posts.published.scopes.Community: self._make_published_post_community_scope,
            })

        def make_post_type(self, data: Mapping[str, Any]) -> posts.consts.POST.TYPE:
            name, _ = parse_name_and_info(data)
            return self.POST_TYPE_FROM_ID_MAP[name]

        POST_TYPE_FROM_ID_MAP = invert_dict({
            posts.consts.POST.TYPE.PAGE: 'page',
            posts.consts.POST.TYPE.IMAGE: 'image',
            posts.consts.POST.TYPE.VIDEO: 'video',
            posts.consts.POST.TYPE.EVENT: 'event',
            posts.consts.POST.TYPE.PLACE: 'place',
            posts.consts.POST.TYPE.HOW_TO: 'how-to',
            posts.consts.POST.TYPE.RECIPE: 'recipe',
            posts.consts.POST.TYPE.PRODUCT: 'product',
        })
        assert set(POST_TYPE_FROM_ID_MAP.values()) == posts.consts.POST.TYPE.ALL

        def make_post_status(self, data: Mapping[str, Any]):
            name, info = parse_name_and_info(data)
            status = self.POST_STATUS_FROM_ID_MAP[name]
            return self.post_status_to_factory_func_map[status](info)

        POST_STATUS_FROM_ID_MAP = invert_dict(ensure_map_is_complete(posts.statuses.Status, {
            posts.statuses.Draft: 'draft',
            posts.statuses.Published: 'published',
            posts.statuses.Removed: 'removed',
        }))

        def _make_draft_post_status(self, data: Mapping[str, Any]):
            return posts.statuses.Draft(stage=self._make_draft_post_stage(data['stage']))

        def _make_draft_post_stage(self, data: Mapping[str, Any]):
            name, info = parse_name_and_info(data)
            stage = self.DRAFT_POST_STAGE_FROM_ID_MAP[name]
            return self.draft_post_stage_to_factory_func_map[stage](info)

        DRAFT_POST_STAGE_FROM_ID_MAP = invert_dict(ensure_map_is_complete(posts.drafts.stages.Stage, {
            posts.drafts.stages.Created: 'created',
            posts.drafts.stages.InProgress: 'in_progress',
            posts.drafts.stages.InReview: 'in_review',
            posts.drafts.stages.Ready: 'ready',
        }))

        @staticmethod
        def _make_draft_post_created_stage(data: Mapping[str, Any]):
            return posts.drafts.stages.Created(is_imported=bool(data['is_imported']))

        @staticmethod
        def _make_draft_post_in_progress_stage(data: Mapping[str, Any]):
            return posts.drafts.stages.InProgress(is_rejected=bool(data['is_rejected']))

        def _make_published_post_status(self, data: Mapping[str, Any]):
            return posts.statuses.Published(scope=self._make_published_post_scope(data['scope']))

        def _make_published_post_scope(self, data: Mapping[str, Any]):
            name, info = parse_name_and_info(data)
            scope = self.PUBLISHED_POST_SCOPE_FROM_ID_MAP[name]
            return self.published_post_scope_to_factory_func_map[scope](info)

        PUBLISHED_POST_SCOPE_FROM_ID_MAP = invert_dict(ensure_map_is_complete(
            posts.published.scopes.Scope, {
                posts.published.scopes.Site: 'site',
                posts.published.scopes.Community: 'community',
            })
        )

        @staticmethod
        def _make_published_post_site_scope(data: Mapping[str, Any]):
            return posts.published.scopes.Site(is_promoted=bool(data['is_promoted']))

        @staticmethod
        def _make_published_post_community_scope(data: Mapping[str, Any]):
            return posts.published.scopes.Community(is_demoted=bool(data['is_demoted']))

    class Users:
        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.user_status_to_factory_func_map = ensure_map_is_complete(users.statuses.Status, {
                users.statuses.Active: lambda _: users.statuses.Active(),
                users.statuses.Pending: lambda _: users.statuses.Pending(),
                users.statuses.Inactive: self._make_inactive_user_profile_status,
            })

        def make_user_profile_status(self, data: Mapping[str, Any]):
            name, info = parse_name_and_info(data)
            status = self.USER_PROFILE_STATUS_FROM_ID_MAP[name]
            return self.user_status_to_factory_func_map[status](info)

        USER_PROFILE_STATUS_FROM_ID_MAP = invert_dict(ensure_map_is_complete(users.statuses.Status, {
            users.statuses.Active: 'active',
            users.statuses.Pending: 'pending',
            users.statuses.Inactive: 'inactive',
        }))

        @staticmethod
        def _make_inactive_user_profile_status(data: Mapping[str, Any]):
            return users.statuses.Inactive(is_banned=bool(data['is_banned']))

        def make_user_status(self, data: Mapping[str, Any]) -> users.consts.USER.STATUS:
            name, _ = parse_name_and_info(data)
            return self.USER_STATUS_FROM_ID_MAP[name]

        USER_STATUS_FROM_ID_MAP = invert_dict({
            users.consts.USER.STATUS.ACTIVE: 'active',
            users.consts.USER.STATUS.INACTIVE: 'inactive',
        })
        assert set(USER_STATUS_FROM_ID_MAP.values()) == users.consts.USER.STATUS.ALL

    class Texts:
        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.text_to_name_map = ensure_map_is_complete(Text, {
                posts.texts.Titles: 'post-titles',
                posts.texts.Subtitles: 'post-subtitles',
                posts.texts.RegularTags: 'post-regular-tags',
                posts.texts.Bodies: 'post-bodies',
                posts.texts.CustomField: 'custom-post-field',

                users.texts.Titles: 'user-titles',
                users.texts.Emails: 'user-emails',
                users.texts.AboutHtml: 'user-about-html',
                users.texts.Description: 'user-description',
                users.texts.CustomField: 'custom-user-field',
            })
            self.text_from_name_map = invert_dict(self.text_to_name_map)
            self.text_to_info_func_map = ensure_map_is_complete(Text, {
                posts.texts.Titles: lambda _: dict(),
                posts.texts.Subtitles: lambda _: dict(),
                posts.texts.RegularTags: lambda _: dict(),
                posts.texts.Bodies: lambda _: dict(),
                posts.texts.CustomField: self._jsonify_custom_post_field,

                users.texts.Titles: lambda _: dict(),
                users.texts.Emails: lambda _: dict(),
                users.texts.AboutHtml: lambda _: dict(),
                users.texts.Description: lambda _: dict(),
                users.texts.CustomField: self._jsonify_custom_user_field,
            })
            self.text_to_factory_func_map = ensure_map_is_complete(Text, {
                posts.texts.Titles: lambda _: posts.texts.Titles(),
                posts.texts.Subtitles: lambda _: posts.texts.Subtitles(),
                posts.texts.RegularTags: lambda _: posts.texts.RegularTags(),
                posts.texts.Bodies: lambda _: posts.texts.Bodies(),
                posts.texts.CustomField: self._make_custom_post_field,

                users.texts.Titles: lambda _: users.texts.Titles(),
                users.texts.Emails: lambda _: users.texts.Emails(),
                users.texts.AboutHtml: lambda _: users.texts.AboutHtml(),
                users.texts.Description: lambda _: users.texts.Description(),
                users.texts.CustomField: self._make_custom_user_field,
            })

        def jsonify_text(self, text: Text) -> Mapping[str, Any]:
            name = self.text_to_name_map[type(text)]
            info = self.text_to_info_func_map[type(text)](text)
            return {name: info}

        def make_text(self, data: Mapping[str, Any]) -> Text:
            name, info = parse_name_and_info(data)
            text_type = self.text_from_name_map[name]
            return self.text_to_factory_func_map[text_type](info)

        @staticmethod
        def _jsonify_custom_post_field(text: posts.texts.CustomField):
            return {'path': text.path}

        @staticmethod
        def _make_custom_post_field(data: Mapping[str, Any]) -> posts.texts.CustomField:
            return posts.texts.CustomField(path=str(data['path']))

        @staticmethod
        def _jsonify_custom_user_field(text: users.texts.CustomField):
            return {'path': text.path}

        @staticmethod
        def _make_custom_user_field(data: Mapping[str, Any]) -> users.texts.CustomField:
            return users.texts.CustomField(path=str(data['path']))

    class Labels:
        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.label_name_to_label_map = invert_dict(ensure_map_is_complete(Label, {
                posts.labels.Id: 'post-id',
                posts.labels.Type: 'post-type',
                posts.labels.Status: 'post-status',
                posts.labels.Private: 'private-post',
                posts.labels.Suspicious: 'suspicious-post',
                posts.labels.PrimaryTag: 'post-primary-tag',
                posts.labels.RegularTag: 'post-regular-tag',
                posts.labels.PrimarySection: 'post-primary-section',
                posts.labels.RegularSection: 'post-regular-section',
                posts.labels.Community: 'post-community',
                posts.labels.Author: 'post-author',
                posts.labels.Stage: 'post-stage',
                posts.labels.NoPrimaryTags: 'post-without-primary-tags',
                posts.labels.NoRegularTags: 'post-without-regular-tags',
                posts.labels.NoPrimarySections: 'post-without-primary-sections',
                posts.labels.NoRegularSections: 'post-without-regular-sections',
                posts.labels.NoCommunities: 'post-without-communities',
                posts.labels.NoAuthors: 'post-without-authors',
                posts.labels.NoStages: 'post-without-stages',
                posts.labels.CustomField: 'post-custom-field',
                posts.labels.NoCustomField: 'post-without-custom-field',
                posts.labels.DefaultPageLayout: 'default-post-page-layout',
                posts.labels.SpecialPageLayout: 'special-post-page-layout',
                posts.labels.DefaultEditorLayout: 'default-post-editor-layout',
                posts.labels.SpecialEditorLayout: 'special-post-editor-layout',

                users.labels.Id: 'user-id',
                users.labels.Owner: 'user-owner',
                users.labels.Status: 'user-status',
                users.labels.UserGroup: 'user-group',
                users.labels.Community: 'user-community',
                users.labels.AccessRole: 'user-access-role',
                users.labels.NoUserGroups: 'user-without-groups',
                users.labels.NoCommunities: 'user-without-communities',
                users.labels.NoAccessRoles: 'user-without-access-roles',
                users.labels.CustomField: 'user-custom-field',
                users.labels.NoCustomField: 'user-without-custom-field',
            }))
            self.label_to_factory_func_map = ensure_map_is_complete(Label, {
                posts.labels.Id: self._make_post_id,
                posts.labels.Type: self._make_post_type,
                posts.labels.Status: self._make_post_status,
                posts.labels.Private: lambda _: posts.labels.Private(),
                posts.labels.Suspicious: lambda _: posts.labels.Suspicious(),
                posts.labels.PrimaryTag: self._make_primary_post_tag,
                posts.labels.RegularTag: self._make_regular_post_tag,
                posts.labels.PrimarySection: self._make_primary_post_section,
                posts.labels.RegularSection: self._make_regular_post_section,
                posts.labels.Community: self._make_post_community,
                posts.labels.Author: self._make_post_author,
                posts.labels.Stage: self._make_post_stage,
                posts.labels.NoPrimaryTags: lambda _: posts.labels.NoPrimaryTags(),
                posts.labels.NoRegularTags: lambda _: posts.labels.NoRegularTags(),
                posts.labels.NoPrimarySections: lambda _: posts.labels.NoPrimarySections(),
                posts.labels.NoRegularSections: lambda _: posts.labels.NoRegularSections(),
                posts.labels.NoCommunities: lambda _: posts.labels.NoCommunities(),
                posts.labels.NoAuthors: lambda _: posts.labels.NoAuthors(),
                posts.labels.NoStages: lambda _: posts.labels.NoStages(),
                posts.labels.CustomField: self._make_custom_post_field,
                posts.labels.NoCustomField: self._make_no_custom_post_field,
                posts.labels.DefaultPageLayout: lambda _: posts.labels.DefaultPageLayout(),
                posts.labels.SpecialPageLayout: self._make_special_post_page_layout,
                posts.labels.DefaultEditorLayout: lambda _: posts.labels.DefaultEditorLayout(),
                posts.labels.SpecialEditorLayout: self._make_special_post_editor_layout,

                users.labels.Id: self._make_user_profile_id,
                users.labels.Owner: self._make_user_profile_owner,
                users.labels.Status: self._make_user_profile_status,
                users.labels.UserGroup: self._make_user_group,
                users.labels.Community: self._make_user_community,
                users.labels.AccessRole: self._make_user_access_role,
                users.labels.NoUserGroups: lambda _: users.labels.NoUserGroups(),
                users.labels.NoCommunities: lambda _: users.labels.NoCommunities(),
                users.labels.NoAccessRoles: lambda _: users.labels.NoAccessRoles(),
                users.labels.CustomField: self._make_custom_user_profile_field,
                users.labels.NoCustomField: self._make_no_custom_user_profile_field,
            })

        def stream_labels(self, data: Iterable[Mapping[str, Any]]) -> Iterator[Label]:
            return map(self._make_label, data)

        def _make_label(self, data: Mapping[str, Any]) -> Label:
            name, info = parse_name_and_info(data)
            label_type = self.label_name_to_label_map[name]
            return self.label_to_factory_func_map[label_type](info)

        @staticmethod
        def _make_post_id(data: Any):
            return posts.labels.Id(value=int(data))

        def _make_post_type(self, data: Any):
            return posts.labels.Type(type=self.protocol.posts.make_post_type(data))

        def _make_post_status(self, data: Any):
            return posts.labels.Status(status=self.protocol.posts.make_post_status(data))

        @staticmethod
        def _make_primary_post_tag(data: Any):
            return posts.labels.PrimaryTag(slug=str(data['slug']))

        @staticmethod
        def _make_regular_post_tag(data: Any):
            return posts.labels.RegularTag(slug=str(data['slug']))

        @staticmethod
        def _make_primary_post_section(data: Any):
            return posts.labels.PrimarySection(id=int(data['id']))

        @staticmethod
        def _make_regular_post_section(data: Any):
            return posts.labels.RegularSection(id=int(data['id']))

        @staticmethod
        def _make_post_community(data: Any):
            return posts.labels.Community(id=int(data['id']))

        @staticmethod
        def _make_post_author(data: Any):
            return posts.labels.Author(id=int(data['id']))

        @staticmethod
        def _make_post_stage(data: Any):
            return posts.labels.Stage(id=int(data['id']))

        @staticmethod
        def _make_custom_post_field(data: Any):
            return posts.labels.CustomField(path=str(data['path']), value=data['value'])

        @staticmethod
        def _make_no_custom_post_field(data: Any):
            return posts.labels.NoCustomField(path=str(data['path']))

        @staticmethod
        def _make_special_post_page_layout(data: Any):
            return posts.labels.SpecialPageLayout(slug=str(data['slug']))

        @staticmethod
        def _make_special_post_editor_layout(data: Any):
            return posts.labels.SpecialEditorLayout(slug=str(data['slug']))

        @staticmethod
        def _make_user_profile_id(data: Any):
            return users.labels.Id(value=int(data))

        @staticmethod
        def _make_user_profile_owner(data: Any):
            return users.labels.Owner(user_id=int(data['user_id']))

        def _make_user_profile_status(self, data: Any):
            return users.labels.Status(status=self.protocol.users.make_user_profile_status(data))

        @staticmethod
        def _make_user_group(data: Any):
            return users.labels.UserGroup(slug=str(data['slug']))

        @staticmethod
        def _make_user_community(data: Any):
            return users.labels.Community(id=int(data['id']))

        @staticmethod
        def _make_user_access_role(data: Any):
            return users.labels.AccessRole(id=int(data['id']))

        @staticmethod
        def _make_custom_user_profile_field(data: Any):
            return users.labels.CustomField(path=str(data['path']), value=data['value'])

        @staticmethod
        def _make_no_custom_user_profile_field(data: Any):
            return users.labels.NoCustomField(path=str(data['path']))

    class Fields:
        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.field_to_name_map = ensure_map_is_complete(Field, {
                posts.fields.ModifiedAt: 'post-modified-at',
                posts.fields.ScheduledAt: 'post-scheduled-at',
                posts.fields.PublishedAt: 'post-published-at',
                posts.fields.LifetimePageViews: 'lifetime-post-page-views',
                posts.fields.Metric: NotImplemented,
                posts.fields.CustomField: 'custom-post-field',

                users.fields.Title: 'user-profile-title',
                users.fields.LastLoggedInAt: 'user-last-logged-in-at',
                users.fields.LifetimePosts: 'lifetime-user-posts',
                users.fields.CustomField: 'custom-user-field',
            })
            self.field_from_name_map = invert_dict(self.field_to_name_map)
            self.field_to_factory_func_map = ensure_map_is_complete(Field, {
                posts.fields.ModifiedAt: lambda _: posts.fields.ModifiedAt(),
                posts.fields.ScheduledAt: lambda _: posts.fields.ScheduledAt(),
                posts.fields.PublishedAt: lambda _: posts.fields.PublishedAt(),
                posts.fields.LifetimePageViews: lambda _: posts.fields.LifetimePageViews(),
                posts.fields.Metric: NotImplemented,
                posts.fields.CustomField: self._make_custom_post_field,

                users.fields.Title: lambda _: users.fields.Title(),
                users.fields.LastLoggedInAt: lambda _: users.fields.LastLoggedInAt(),
                users.fields.LifetimePosts: lambda _: users.fields.LifetimePosts(),
                users.fields.CustomField: self._make_custom_user_field,
            })
            self.field_to_jsonify_info_func_map = ensure_map_is_complete(Field, {
                posts.fields.ModifiedAt: lambda _: dict(),
                posts.fields.ScheduledAt: lambda _: dict(),
                posts.fields.PublishedAt: lambda _: dict(),
                posts.fields.LifetimePageViews: lambda _: dict(),
                posts.fields.Metric: NotImplemented,
                posts.fields.CustomField: self._jsonify_custom_post_field,

                users.fields.Title: lambda _: dict(),
                users.fields.LastLoggedInAt: lambda _: dict(),
                users.fields.LifetimePosts: lambda _: dict(),
                users.fields.CustomField: self._jsonify_custom_user_field,
            })

        def stream_ranges(self, data: Iterable[Mapping[str, Any]]) -> Iterator[Range]:
            return map(self._make_range, data)

        def _make_range(self, data: Mapping[str, Any]) -> Range:
            return Range(
                field=self.make_field(data['field']),
                min_value=data['min'],
                max_value=data['max'],
            )

        def make_field(self, data: Mapping[str, Any]) -> Field:
            name, info = parse_name_and_info(data)
            field_type = self.field_from_name_map[name]
            return self.field_to_factory_func_map[field_type](info)

        def jsonify_field(self, field: Field) -> Mapping[str, Any]:
            name = self.field_to_name_map[type(field)]
            info = self.field_to_jsonify_info_func_map[type(field)](field)
            return {name: info}

        @staticmethod
        def _make_custom_post_field(data: Any):
            return posts.fields.CustomField(path=str(data['path']))

        @staticmethod
        def _jsonify_custom_post_field(field: posts.fields.CustomField):
            return {'path': field.path}

        @staticmethod
        def _make_custom_user_field(data: Any):
            return users.fields.CustomField(path=str(data['path']))

        @staticmethod
        def _jsonify_custom_user_field(field: users.fields.CustomField):
            return {'path': field.path}

    class Orders:
        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.order_name_order_map = invert_dict(ensure_map_is_complete(Order, {
                orders.Value: 'value',
                orders.Relevance: 'relevance',
            }))
            self.order_order_to_factory_func_map = ensure_map_is_complete(Order, {
                orders.Value: self._make_order_by_value,
                orders.Relevance: self._make_order_by_relevance,
            })

        def make_order(self, data: Mapping[str, Any]) -> Order:
            name, info = parse_name_and_info(data)
            order_type = self.order_name_order_map[name]
            return self.order_order_to_factory_func_map[order_type](info)

        def _make_order_by_value(self, data: Mapping[str, Any]):
            return orders.Value(
                field=self.protocol.fields.make_field(data['field']),
                reverse=bool(data['reverse']),
            )

        def _make_order_by_relevance(self, data: Mapping[str, Any]):
            return orders.Relevance(
                decay=unless_none(self._make_decay)(data.get('decay')),
            )

        def _make_decay(self, data: Mapping[str, Any]):
            return orders.Decay(
                field=self.protocol.fields.make_field(data['field']),
                speed=float(data['speed']),
            )

    class Filters:
        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.filter_name_to_filter_map = invert_dict(ensure_map_is_complete(Filter, {
                filters.AnyLabel: 'any_label',
                filters.NoLabels: 'no_labels',
                filters.AnyRange: 'any_range',
                filters.NoRanges: 'no_ranges',
                filters.Phrase: 'phrase',
            }))
            self.filter_to_factory_func_map = ensure_map_is_complete(Filter, {
                filters.AnyLabel: self._make_any_label_filter,
                filters.NoLabels: self._make_no_labels_filter,
                filters.AnyRange: self._make_any_range_filter,
                filters.NoRanges: self._make_no_ranges_filter,
                filters.Phrase: self._make_phrase_filter,
            })

        def make_filters(self, data: Iterable[Mapping[str, Any]]) -> AbstractSet[Filter]:
            return frozenset(map(self._make_filter, data))

        def _make_filter(self, data: Mapping[str, Any]) -> Filter:
            name, info = parse_name_and_info(data)
            filter_type = self.filter_name_to_filter_map[name]
            return self.filter_to_factory_func_map[filter_type](info)

        def _make_any_label_filter(self, data: Any):
            return filters.AnyLabel(labels=tuple(self.protocol.labels.stream_labels(data)))

        def _make_no_labels_filter(self, data: Any):
            return filters.NoLabels(labels=tuple(self.protocol.labels.stream_labels(data)))

        def _make_any_range_filter(self, data: Any):
            return filters.AnyRange(ranges=tuple(self.protocol.fields.stream_ranges(data)))

        def _make_no_ranges_filter(self, data: Any):
            return filters.NoRanges(ranges=tuple(self.protocol.fields.stream_ranges(data)))

        @staticmethod
        def _make_phrase_filter(data: Mapping[str, Any]):
            return filters.Phrase(
                phrase=str(data['phrase']),
                syntax=unless_none(apply(read_only, dict))(data.get('syntax')),
                weights=unless_none(lambda weights: tuple(map(int, weights)))(data.get('weights')),
            )

    class Conditions:
        def __init__(self):
            self.condition_to_name_map = ensure_map_is_complete(Condition, {
                posts.conditions.IsDraft: 'post-is-draft',
                posts.conditions.IsRemoved: 'post-is-removed',
                posts.conditions.IsPublished: 'post-is-published',
            })
            self.condition_from_name_map = invert_dict(self.condition_to_name_map)

        def jsonify_condition(self, condition: Condition) -> Mapping[str, Any]:
            name = self.condition_to_name_map[type(condition)]
            return {name: {}}

        def make_condition(self, data: Mapping[str, Any]) -> Condition:
            name, _ = parse_name_and_info(data)
            return self.condition_from_name_map[name]()
