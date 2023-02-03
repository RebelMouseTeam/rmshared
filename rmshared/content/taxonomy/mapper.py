from itertools import chain
from typing import Any
from typing import Iterable
from typing import Iterator
from typing import Mapping

from rmshared.tools import ensure_map_is_complete
from rmshared.tools import invert_dict
from rmshared.tools import parse_name_and_info
from rmshared.tools import unless_none
from rmshared.typings import read_only

from rmshared.content.taxonomy import core
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


class Mapper:
    def __init__(self):
        self.posts = self.Posts()
        self.users = self.Users()
        self.texts = self.Texts(self)
        self.labels = self.Labels(self)
        self.ranges = self.Ranges(self)
        self.fields = self.Fields(self)
        self.orders = self.Orders(self)
        self.filters = self.Filters(self)
        self.conditions = self.Conditions()

    class Posts:
        def __init__(self):
            self.post_status_to_factory_func_map = ensure_map_is_complete(posts.statuses.Status, {
                posts.statuses.Draft: self._map_draft_post_status,
                posts.statuses.Published: self._map_published_post_status,
                posts.statuses.Removed: lambda _: 'removed',
            })
            self.draft_post_stage_to_factory_func_map = ensure_map_is_complete(posts.drafts.stages.Stage, {
                posts.drafts.stages.Created: self._map_draft_post_created_stage,
                posts.drafts.stages.InProgress: self._map_draft_post_in_progress_stage,
                posts.drafts.stages.InReview: lambda _: 'in-review',
                posts.drafts.stages.Ready: lambda _: 'ready',
            })
            self.published_post_scope_to_factory_func_map = ensure_map_is_complete(posts.published.scopes.Scope, {
                posts.published.scopes.Site: self._map_published_post_site_scope,
                posts.published.scopes.Community: self._map_published_post_community_scope,
            })

        def map_post_type(self, type_: posts.consts.POST.TYPE) -> str:
            return self.POST_TYPE_TO_ID_MAP[type_]

        POST_TYPE_TO_ID_MAP = {
            posts.consts.POST.TYPE.PAGE: 'page',
            posts.consts.POST.TYPE.IMAGE: 'image',
            posts.consts.POST.TYPE.VIDEO: 'video',
            posts.consts.POST.TYPE.EVENT: 'event',
            posts.consts.POST.TYPE.PLACE: 'place',
            posts.consts.POST.TYPE.HOW_TO: 'how-to',
            posts.consts.POST.TYPE.RECIPE: 'recipe',
            posts.consts.POST.TYPE.PRODUCT: 'product',
        }
        assert set(POST_TYPE_TO_ID_MAP.keys()) == posts.consts.POST.TYPE.ALL

        def map_post_status(self, status: posts.statuses.Status) -> str:
            return self.post_status_to_factory_func_map[type(status)](status)

        def _map_draft_post_status(self, status: posts.statuses.Draft) -> str:
            return f'draft-{self._map_draft_post_stage(status.stage)}'

        def _map_draft_post_stage(self, stage: posts.drafts.stages.Stage) -> str:
            return self.draft_post_stage_to_factory_func_map[type(stage)](stage)

        @staticmethod
        def _map_draft_post_created_stage(stage: posts.drafts.stages.Created) -> str:
            return f'created(imported={str(stage.is_imported).lower()})'

        @staticmethod
        def _map_draft_post_in_progress_stage(stage: posts.drafts.stages.InProgress) -> str:
            return f'in-progress(rejected={str(stage.is_rejected).lower()})'

        def _map_published_post_status(self, status: posts.statuses.Published) -> str:
            return f'published-to-{self._map_published_post_scope(status.scope)}'

        def _map_published_post_scope(self, scope: posts.published.scopes.Scope) -> str:
            return self.published_post_scope_to_factory_func_map[type(scope)](scope)

        @staticmethod
        def _map_published_post_site_scope(scope: posts.published.scopes.Site) -> str:
            return f'site(promoted={str(scope.is_promoted).lower()})'

        @staticmethod
        def _map_published_post_community_scope(scope: posts.published.scopes.Community) -> str:
            return f'community(demoted={str(scope.is_demoted).lower()})'

    class Users:
        def __init__(self):
            self.user_status_to_factory_func_map = ensure_map_is_complete(users.statuses.Status, {
                users.statuses.Active: lambda _: 'active',
                users.statuses.Pending: lambda _: 'pending',
                users.statuses.Inactive: self._map_inactive_user_profile_status,
            })

        def map_user_profile_status(self, status: users.statuses.Status) -> str:
            return self.user_status_to_factory_func_map[type(status)](status)

        @staticmethod
        def _map_inactive_user_profile_status(status: users.statuses.Inactive) -> str:
            return f'inactive(banned={str(status.is_banned).lower()})'

        def map_user_status(self, status: users.consts.USER.STATUS) -> str:
            return self.USER_STATUS_TO_ID_MAP[status]

        USER_STATUS_TO_ID_MAP = {
            users.consts.USER.STATUS.ACTIVE: 'active',
            users.consts.USER.STATUS.INACTIVE: 'inactive',
        }
        assert set(USER_STATUS_TO_ID_MAP.keys()) == users.consts.USER.STATUS.ALL

    class Texts:
        def __init__(self, mapper: 'Mapper'):
            self.mapper = mapper
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
                posts.texts.CustomField: self._map_custom_post_field,

                users.texts.Titles: lambda _: users.texts.Titles(),
                users.texts.Emails: lambda _: users.texts.Emails(),
                users.texts.AboutHtml: lambda _: users.texts.AboutHtml(),
                users.texts.Description: lambda _: users.texts.Description(),
                users.texts.CustomField: self._map_custom_user_field,
            })

        def jsonify_text(self, text: Text) -> Mapping[str, Any]:
            name = self.text_to_name_map[type(text)]
            info = self.text_to_info_func_map[type(text)](text)
            return {name: info}

        def map_text(self, data: Mapping[str, Any]) -> Text:
            name, info = parse_name_and_info(data)
            text_type = self.text_from_name_map[name]
            return self.text_to_factory_func_map[text_type](info)

        @staticmethod
        def _jsonify_custom_post_field(text: posts.texts.CustomField):
            return {'path': text.path}

        @staticmethod
        def _map_custom_post_field(data: Mapping[str, Any]) -> posts.texts.CustomField:
            return posts.texts.CustomField(path=str(data['path']))

        @staticmethod
        def _jsonify_custom_user_field(text: users.texts.CustomField):
            return {'path': text.path}

        @staticmethod
        def _map_custom_user_field(data: Mapping[str, Any]) -> users.texts.CustomField:
            return users.texts.CustomField(path=str(data['path']))

    class Labels:
        def __init__(self, mapper: 'Mapper'):
            self.mapper = mapper
            self.label_to_factory_func_map = ensure_map_is_complete(Label, {
                posts.labels.Id: self._map_post_id,
                posts.labels.Type: self._map_post_type,
                posts.labels.Status: self._map_post_status,
                posts.labels.Private: lambda _: core.labels.Badge(field=core.Field('private-post')),
                posts.labels.Suspicious: lambda _: core.labels.Badge(field=core.Field('suspicious-post')),
                posts.labels.PrimaryTag: self._map_primary_post_tag,
                posts.labels.RegularTag: self._map_regular_post_tag,
                posts.labels.PrimarySection: self._map_primary_post_section,
                posts.labels.RegularSection: self._map_regular_post_section,
                posts.labels.Community: self._map_post_community,
                posts.labels.Author: self._map_post_author,
                posts.labels.Stage: self._map_post_stage,
                posts.labels.NoPrimaryTags: lambda _: core.labels.Empty(field=core.Field('post-primary-tag')),
                posts.labels.NoRegularTags: lambda _: core.labels.Empty(field=core.Field('post-regular-tag')),
                posts.labels.NoPrimarySections: lambda _: core.labels.Empty(field=core.Field('post-primary-section')),
                posts.labels.NoRegularSections: lambda _: core.labels.Empty(field=core.Field('post-regular-section')),
                posts.labels.NoCommunities: lambda _: core.labels.Empty(field=core.Field('post-community')),
                posts.labels.NoAuthors: lambda _: core.labels.Empty(field=core.Field('post-author')),
                posts.labels.NoStages: lambda _: core.labels.Empty(field=core.Field('post-stage')),
                posts.labels.CustomField: self._map_custom_post_field,
                posts.labels.NoCustomField: self._map_no_custom_post_field,
                posts.labels.DefaultPageLayout: lambda _: core.labels.Empty(field=core.Field('post-page-layout')),
                posts.labels.SpecialPageLayout: self._map_special_post_page_layout,
                posts.labels.DefaultEditorLayout: lambda _: core.labels.Empty(field=core.Field('post-editor-layout')),
                posts.labels.SpecialEditorLayout: self._map_special_post_editor_layout,

                users.labels.Id: self._map_user_profile_id,
                users.labels.Owner: self._map_user_profile_owner,
                users.labels.Status: self._map_user_profile_status,
                users.labels.UserGroup: self._map_user_group,
                users.labels.Community: self._map_user_community,
                users.labels.AccessRole: self._map_user_access_role,
                users.labels.NoUserGroups: lambda _: core.labels.Empty(field=core.Field('user-group')),
                users.labels.NoCommunities: lambda _: core.labels.Empty(field=core.Field('user-community')),
                users.labels.NoAccessRoles: lambda _: core.labels.Empty(field=core.Field('user-access-role')),
                users.labels.CustomField: self._map_custom_user_profile_field,
                users.labels.NoCustomField: self._map_no_custom_user_profile_field,
            })

        def map_label(self, label: Label) -> core.Label:
            return self.label_to_factory_func_map[type(label)](label)

        @staticmethod
        def _map_post_id(label: posts.labels.Id) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-id'), value=label.value)

        def _map_post_type(self, label: posts.labels.Type) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-type'), value=self.mapper.posts.map_post_type(label.type))

        def _map_post_status(self, label: posts.labels.Status) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-status'), value=self.mapper.posts.map_post_status(label.status))

        @staticmethod
        def _map_primary_post_tag(label: posts.labels.PrimaryTag) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-primary-tag'), value=label.slug)

        @staticmethod
        def _map_regular_post_tag(label: posts.labels.RegularTag) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-regular-tag'), value=label.slug)

        @staticmethod
        def _map_primary_post_section(label: posts.labels.PrimarySection) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-primary-section'), value=label.id)

        @staticmethod
        def _map_regular_post_section(label: posts.labels.RegularSection) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-regular-section'), value=label.id)

        @staticmethod
        def _map_post_community(label: posts.labels.Community) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-community'), value=label.id)

        @staticmethod
        def _map_post_author(label: posts.labels.Author) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-author'), value=label.id)

        @staticmethod
        def _map_post_stage(label: posts.labels.Stage) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-stage'), value=label.id)

        @staticmethod
        def _map_custom_post_field(label: posts.labels.CustomField) -> core.labels.Value:
            return core.labels.Value(field=core.Field(f'custom-post-field({label.path})'), value=label.value)

        @staticmethod
        def _map_no_custom_post_field(label: posts.labels.NoCustomField) -> core.labels.Empty:
            return core.labels.Empty(field=core.Field(f'custom-post-field({label.path})'))

        @staticmethod
        def _map_special_post_page_layout(label: posts.labels.SpecialPageLayout) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-page-layout'), value=label.slug)

        @staticmethod
        def _map_special_post_editor_layout(label: posts.labels.SpecialEditorLayout) -> core.labels.Value:
            return core.labels.Value(field=core.Field('post-editor-layout'), value=label.slug)

        @staticmethod
        def _map_user_profile_id(label: users.labels.Id) -> core.labels.Value:
            return core.labels.Value(field=core.Field('user-id'), value=label.value)

        @staticmethod
        def _map_user_profile_owner(label: users.labels.Owner) -> core.labels.Value:
            return core.labels.Value(field=core.Field('user-owner'), value=label.user_id)

        def _map_user_profile_status(self, label: users.labels.Status) -> core.labels.Value:
            return core.labels.Value(field=core.Field('user-status'), value=self.mapper.users.map_user_profile_status(label.status))

        @staticmethod
        def _map_user_group(label: users.labels.UserGroup) -> core.labels.Value:
            return core.labels.Value(field=core.Field('user-group'), value=label.slug)

        @staticmethod
        def _map_user_community(label: users.labels.Community) -> core.labels.Value:
            return core.labels.Value(field=core.Field('user-community'), value=label.id)

        @staticmethod
        def _map_user_access_role(label: users.labels.AccessRole) -> core.labels.Value:
            return core.labels.Value(field=core.Field('user-access-role'), value=label.id)

        @staticmethod
        def _map_custom_user_profile_field(label: users.labels.CustomField) -> core.labels.Value:
            return core.labels.Value(field=core.Field(f'custom-user-field({label.path})'), value=label.value)

        @staticmethod
        def _map_no_custom_user_profile_field(label: users.labels.NoCustomField) -> core.labels.Empty:
            return core.labels.Empty(field=core.Field(f'custom-user-field({label.path})'))

    class Ranges:
        def __init__(self, mapper: 'Mapper'):
            self.mapper = mapper

        def map_range(self, range_: Range) -> Iterable[core.Range]:
            field = self.mapper.fields.map_field(range_.field)
            if None not in {range_.min_value, range_.max_value}:
                yield core.ranges.Between(field, min_value=range_.min_value, max_value=range_.max_value)
            elif range_.max_value is not None:
                yield core.ranges.LessThan(field, value=range_.max_value)
            elif range_.min_value is not None:
                yield core.ranges.MoreThan(field, value=range_.min_value)
            else:
                return []

    class Fields:
        def __init__(self, mapper: 'Mapper'):
            self.mapper = mapper
            self.field_to_factory_func_map = ensure_map_is_complete(Field, {
                posts.fields.ModifiedAt: lambda _: core.Field('post-modified-at'),
                posts.fields.ScheduledAt: lambda _: core.Field('post-scheduled-at'),
                posts.fields.PublishedAt: lambda _: core.Field('post-published-at'),
                posts.fields.Metric: NotImplemented,
                posts.fields.LifetimePageViews: lambda _: core.Field('lifetime-post-page-views'),
                posts.fields.CustomField: self._map_custom_post_field,

                users.fields.Title: lambda _: core.Field('user-profile-title'),
                users.fields.LastLoggedInAt: lambda _: core.Field('user-last-logged-in-at'),
                users.fields.LifetimePosts: lambda _: core.Field('lifetime-user-posts'),
                users.fields.CustomField: self._map_custom_user_field,
            })

        def map_field(self, field: Field) -> core.Field:
            return self.field_to_factory_func_map[type(field)](field)

        @staticmethod
        def _map_custom_post_field(field: posts.fields.CustomField) -> core.Field:
            return core.Field(f'custom-post-field({field.path})')

        @staticmethod
        def _map_custom_user_field(field: users.fields.CustomField) -> core.Field:
            return core.Field(f'custom-user-field({field.path})')

    class Orders:
        def __init__(self, mapper: 'Mapper'):
            self.mapper = mapper
            self.order_name_order_map = invert_dict(ensure_map_is_complete(Order, {
                orders.Value: 'value',
                orders.Relevance: 'relevance',
            }))
            self.order_order_to_factory_func_map = ensure_map_is_complete(Order, {
                orders.Value: self._map_order_by_value,
                orders.Relevance: self._map_order_by_relevance,
            })

        def map_order(self, data: Mapping[str, Any]) -> Order:
            name, info = parse_name_and_info(data)
            order_type = self.order_name_order_map[name]
            return self.order_order_to_factory_func_map[order_type](info)

        def _map_order_by_value(self, data: Mapping[str, Any]):
            return orders.Value(
                field=self.mapper.fields.map_field(data['field']),
                reverse=bool(data['reverse']),
            )

        def _map_order_by_relevance(self, data: Mapping[str, Any]):
            return orders.Relevance(
                decay=unless_none(self._map_decay)(data.get('decay')),
            )

        def _map_decay(self, data: Mapping[str, Any]):
            return orders.Decay(
                field=self.mapper.fields.map_field(data['field']),
                speed=float(data['speed']),
            )

    class Filters:
        def __init__(self, mapper: 'Mapper'):
            self.mapper = mapper
            self.filter_to_factory_func_map = ensure_map_is_complete(Filter, {
                filters.AnyLabel: self._map_any_label_filter,
                filters.NoLabels: self._map_no_labels_filter,
                filters.AnyRange: self._map_any_range_filter,
                filters.NoRanges: self._map_no_ranges_filter,
                filters.Phrase: self._map_phrase_filter,
            })

        def map_filters(self, filters_: Iterable[Filter]) -> Iterator[core.Filter]:
            return map(self._map_filter, filters_)

        def _map_filter(self, filter_: Filter) -> core.Filter:
            return self.filter_to_factory_func_map[type(filter_)](filter_)

        def _map_any_label_filter(self, filter_: filters.AnyLabel) -> core.filters.AnyLabel:
            return core.filters.AnyLabel(labels=tuple(map(self.mapper.labels.map_label, filter_.labels)))

        def _map_no_labels_filter(self, filter_: filters.NoLabels) -> core.filters.NoLabels:
            return core.filters.NoLabels(labels=tuple(map(self.mapper.labels.map_label, filter_.labels)))

        def _map_any_range_filter(self, filter_: filters.AnyRange) -> core.filters.AnyRange:
            return core.filters.AnyRange(ranges=tuple(chain.from_iterable(map(self.mapper.ranges.map_range, filter_.ranges))))

        def _map_no_ranges_filter(self, filter_: filters.NoRanges) -> core.filters.NoRanges:
            return core.filters.NoRanges(ranges=tuple(chain.from_iterable(map(self.mapper.ranges.map_range, filter_.ranges))))

        @staticmethod
        def _map_phrase_filter(filter_: filters.Phrase) -> core.filters.Phrase:
            return core.filters.Phrase(
                phrase=filter_.phrase,
                payload=read_only({
                    'syntax': filter_.syntax,
                    'weights': filter_.weights,
                }),
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

        def map_condition(self, data: Mapping[str, Any]) -> Condition:
            name, _ = parse_name_and_info(data)
            return self.condition_from_name_map[name]()
