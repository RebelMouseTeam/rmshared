from typing import Any
from typing import Mapping

from rmshared.tools import ensure_map_is_complete
from rmshared.tools import invert_dict
from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import mappers
from rmshared.content.taxonomy.abc import Text
from rmshared.content.taxonomy.abc import Condition

from rmshared.content.taxonomy.posts import labels
from rmshared.content.taxonomy.posts import fields
from rmshared.content.taxonomy.posts import consts
from rmshared.content.taxonomy.posts import statuses
from rmshared.content.taxonomy.posts import drafts
from rmshared.content.taxonomy.posts import published
from rmshared.content.taxonomy.posts import texts
from rmshared.content.taxonomy.posts import conditions


class Labels(mappers.ILabels[labels.Base]):
    def __init__(self, aspects: 'Aspects'):
        self.aspects = aspects
        self.label_to_factory_func_map = ensure_map_is_complete(labels.Base, {
            labels.Id: self._map_post_id,
            labels.Type: self._map_post_type,
            labels.Status: self._map_post_status,
            labels.Private: lambda _: core.labels.Badge(field=core.Field('private-post')),
            labels.Suspicious: lambda _: core.labels.Badge(field=core.Field('suspicious-post')),
            labels.PrimaryTag: self._map_primary_post_tag,
            labels.RegularTag: self._map_regular_post_tag,
            labels.PrimarySection: self._map_primary_post_section,
            labels.RegularSection: self._map_regular_post_section,
            labels.Community: self._map_post_community,
            labels.Author: self._map_post_author,
            labels.Stage: self._map_post_stage,
            labels.NoPrimaryTags: lambda _: core.labels.Empty(field=core.Field('post-primary-tag')),
            labels.NoRegularTags: lambda _: core.labels.Empty(field=core.Field('post-regular-tag')),
            labels.NoPrimarySections: lambda _: core.labels.Empty(field=core.Field('post-primary-section')),
            labels.NoRegularSections: lambda _: core.labels.Empty(field=core.Field('post-regular-section')),
            labels.NoCommunities: lambda _: core.labels.Empty(field=core.Field('post-community')),
            labels.NoAuthors: lambda _: core.labels.Empty(field=core.Field('post-author')),
            labels.NoStages: lambda _: core.labels.Empty(field=core.Field('post-stage')),
            labels.CustomField: self._map_custom_post_field,
            labels.NoCustomField: self._map_no_custom_post_field,
            labels.DefaultPageLayout: lambda _: core.labels.Empty(field=core.Field('post-page-layout')),
            labels.SpecialPageLayout: self._map_special_post_page_layout,
            labels.DefaultEditorLayout: lambda _: core.labels.Empty(field=core.Field('post-editor-layout')),
            labels.SpecialEditorLayout: self._map_special_post_editor_layout,
        })

    def map_label(self, label):
        return self.label_to_factory_func_map[type(label)](label)

    @staticmethod
    def _map_post_id(label: labels.Id) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-id'), value=label.value)

    def _map_post_type(self, label: labels.Type) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-type'), value=self.aspects.map_post_type(label.type))

    def _map_post_status(self, label: labels.Status) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-status'), value=self.aspects.map_post_status(label.status))

    @staticmethod
    def _map_primary_post_tag(label: labels.PrimaryTag) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-primary-tag'), value=label.slug)

    @staticmethod
    def _map_regular_post_tag(label: labels.RegularTag) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-regular-tag'), value=label.slug)

    @staticmethod
    def _map_primary_post_section(label: labels.PrimarySection) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-primary-section'), value=label.id)

    @staticmethod
    def _map_regular_post_section(label: labels.RegularSection) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-regular-section'), value=label.id)

    @staticmethod
    def _map_post_community(label: labels.Community) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-community'), value=label.id)

    @staticmethod
    def _map_post_author(label: labels.Author) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-author'), value=label.id)

    @staticmethod
    def _map_post_stage(label: labels.Stage) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-stage'), value=label.id)

    @staticmethod
    def _map_custom_post_field(label: labels.CustomField) -> core.labels.Value:
        return core.labels.Value(field=core.Field(f'custom-post-field({label.path})'), value=label.value)

    @staticmethod
    def _map_no_custom_post_field(label: labels.NoCustomField) -> core.labels.Empty:
        return core.labels.Empty(field=core.Field(f'custom-post-field({label.path})'))

    @staticmethod
    def _map_special_post_page_layout(label: labels.SpecialPageLayout) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-page-layout'), value=label.slug)

    @staticmethod
    def _map_special_post_editor_layout(label: labels.SpecialEditorLayout) -> core.labels.Value:
        return core.labels.Value(field=core.Field('post-editor-layout'), value=label.slug)


class Fields(mappers.IFields[fields.Base]):
    def __init__(self):
        self.field_to_factory_func_map = ensure_map_is_complete(fields.Base, {
            fields.ModifiedAt: lambda _: core.Field('post-modified-at'),
            fields.ScheduledAt: lambda _: core.Field('post-scheduled-at'),
            fields.PublishedAt: lambda _: core.Field('post-published-at'),
            fields.Metric: NotImplemented,
            fields.LifetimePageViews: lambda _: core.Field('lifetime-post-page-views'),
            fields.CustomField: self._map_custom_post_field,
        })

    def map_field(self, field):
        return self.field_to_factory_func_map[type(field)](field)

    @staticmethod
    def _map_custom_post_field(field: fields.CustomField) -> core.Field:
        return core.Field(f'custom-post-field({field.path})')


class Aspects:
    def __init__(self):
        self.post_status_to_factory_func_map = ensure_map_is_complete(statuses.Status, {
            statuses.Draft: self._map_draft_post_status,
            statuses.Published: self._map_published_post_status,
            statuses.Removed: lambda _: 'removed',
        })
        self.draft_post_stage_to_factory_func_map = ensure_map_is_complete(drafts.stages.Stage, {
            drafts.stages.Created: self._map_draft_post_created_stage,
            drafts.stages.InProgress: self._map_draft_post_in_progress_stage,
            drafts.stages.InReview: lambda _: 'in-review',
            drafts.stages.Ready: lambda _: 'ready',
        })
        self.published_post_scope_to_factory_func_map = ensure_map_is_complete(published.scopes.Scope, {
            published.scopes.Site: self._map_published_post_site_scope,
            published.scopes.Community: self._map_published_post_community_scope,
        })

    def map_post_type(self, type_: consts.POST.TYPE) -> str:
        return self.POST_TYPE_TO_ID_MAP[type_]

    POST_TYPE_TO_ID_MAP = {
        consts.POST.TYPE.PAGE: 'page',
        consts.POST.TYPE.IMAGE: 'image',
        consts.POST.TYPE.VIDEO: 'video',
        consts.POST.TYPE.EVENT: 'event',
        consts.POST.TYPE.PLACE: 'place',
        consts.POST.TYPE.HOW_TO: 'how-to',
        consts.POST.TYPE.RECIPE: 'recipe',
        consts.POST.TYPE.PRODUCT: 'product',
    }
    assert set(POST_TYPE_TO_ID_MAP.keys()) == consts.POST.TYPE.ALL

    def map_post_status(self, status: statuses.Status) -> str:
        return self.post_status_to_factory_func_map[type(status)](status)

    def _map_draft_post_status(self, status: statuses.Draft) -> str:
        return f'draft-{self._map_draft_post_stage(status.stage)}'

    def _map_draft_post_stage(self, stage: drafts.stages.Stage) -> str:
        return self.draft_post_stage_to_factory_func_map[type(stage)](stage)

    @staticmethod
    def _map_draft_post_created_stage(stage: drafts.stages.Created) -> str:
        return f'created(imported={str(stage.is_imported).lower()})'

    @staticmethod
    def _map_draft_post_in_progress_stage(stage: drafts.stages.InProgress) -> str:
        return f'in-progress(rejected={str(stage.is_rejected).lower()})'

    def _map_published_post_status(self, status: statuses.Published) -> str:
        return f'published-to-{self._map_published_post_scope(status.scope)}'

    def _map_published_post_scope(self, scope: published.scopes.Scope) -> str:
        return self.published_post_scope_to_factory_func_map[type(scope)](scope)

    @staticmethod
    def _map_published_post_site_scope(scope: published.scopes.Site) -> str:
        return f'site(promoted={str(scope.is_promoted).lower()})'

    @staticmethod
    def _map_published_post_community_scope(scope: published.scopes.Community) -> str:
        return f'community(demoted={str(scope.is_demoted).lower()})'


class Conditions:
    def __init__(self):
        self.condition_to_name_map = ensure_map_is_complete(Condition, {
            conditions.IsDraft: 'post-is-draft',
            conditions.IsRemoved: 'post-is-removed',
            conditions.IsPublished: 'post-is-published',
        })
        self.condition_from_name_map = invert_dict(self.condition_to_name_map)

    def jsonify_condition(self, condition: Condition) -> Mapping[str, Any]:
        name = self.condition_to_name_map[type(condition)]
        return {name: {}}

    def map_condition(self, data: Mapping[str, Any]) -> Condition:
        name, _ = parse_name_and_info(data)
        return self.condition_from_name_map[name]()


class Texts:
    def __init__(self):
        self.text_to_name_map = ensure_map_is_complete(Text, {
            texts.Titles: 'post-titles',
            texts.Subtitles: 'post-subtitles',
            texts.RegularTags: 'post-regular-tags',
            texts.Bodies: 'post-bodies',
            texts.CustomField: 'custom-post-field',
        })
        self.text_from_name_map = invert_dict(self.text_to_name_map)
        self.text_to_info_func_map = ensure_map_is_complete(Text, {
            texts.Titles: lambda _: dict(),
            texts.Subtitles: lambda _: dict(),
            texts.RegularTags: lambda _: dict(),
            texts.Bodies: lambda _: dict(),
            texts.CustomField: self._jsonify_custom_post_field,
        })
        self.text_to_factory_func_map = ensure_map_is_complete(Text, {
            texts.Titles: lambda _: texts.Titles(),
            texts.Subtitles: lambda _: texts.Subtitles(),
            texts.RegularTags: lambda _: texts.RegularTags(),
            texts.Bodies: lambda _: texts.Bodies(),
            texts.CustomField: self._map_custom_post_field,
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
    def _jsonify_custom_post_field(text: texts.CustomField):
        return {'path': text.path}

    @staticmethod
    def _map_custom_post_field(data: Mapping[str, Any]) -> texts.CustomField:
        return texts.CustomField(path=str(data['path']))
