from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy import core as taxonomy_core
from rmshared.content.taxonomy import visitors as taxonomy_visitors

from rmshared.content.taxonomy.posts import labels
from rmshared.content.taxonomy.posts import fields
from rmshared.content.taxonomy.posts import consts
from rmshared.content.taxonomy.posts import statuses
from rmshared.content.taxonomy.posts import drafts
from rmshared.content.taxonomy.posts import published


class Factory:
    def __init__(self):
        self.delegate = taxonomy_core.mapper.Factory()
        self.aspects = Aspects()

    def make_visitor(self) -> taxonomy_visitors.IVisitor:
        builder = taxonomy_visitors.Builder()
        builder.customize_filters(self.delegate.make_filters, dependencies=(taxonomy_visitors.ILabels, taxonomy_visitors.IRanges))
        builder.customize_labels(self._make_labels, dependencies=())
        builder.customize_ranges(self.delegate.make_ranges, dependencies=(taxonomy_visitors.IValues, ))
        builder.customize_values(self.delegate.make_values, dependencies=())
        return builder.make_visitor()

    def _make_labels(self) -> taxonomy_visitors.ILabels:
        return self.Labels(self.aspects)

    class Labels(taxonomy_visitors.ILabels[labels.Base, taxonomy_core.labels.Label]):
        def __init__(self, aspects: 'Aspects'):
            self.aspects = aspects
            self.label_to_factory_func_map = ensure_map_is_complete(labels.Base, {
                labels.Id: self._map_post_id,
                labels.Type: self._map_post_type,
                labels.Status: self._map_post_status,
                labels.Private: lambda _: taxonomy_core.labels.Badge(field=taxonomy_core.fields.System('post-is-private')),
                labels.Suspicious: lambda _: taxonomy_core.labels.Badge(field=taxonomy_core.fields.System('post-is-suspicious')),
                labels.PrimaryTag: self._map_primary_post_tag,
                labels.RegularTag: self._map_regular_post_tag,
                labels.PrimarySection: self._map_primary_post_section,
                labels.RegularSection: self._map_regular_post_section,
                labels.Community: self._map_post_community,
                labels.Author: self._map_post_author,
                labels.Stage: self._map_post_stage,
                labels.NoPrimaryTags: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('post-primary-tag')),
                labels.NoRegularTags: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('post-regular-tag')),
                labels.NoPrimarySections: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('post-primary-section')),
                labels.NoRegularSections: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('post-regular-section')),
                labels.NoCommunities: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('post-community')),
                labels.NoAuthors: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('post-author')),
                labels.NoStages: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('post-stage')),
                labels.CustomField: self._map_custom_post_field,
                labels.NoCustomField: self._map_no_custom_post_field,
                labels.DefaultPageLayout: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('post-page-layout')),
                labels.SpecialPageLayout: self._map_special_post_page_layout,
                labels.DefaultEditorLayout: lambda _: taxonomy_core.labels.Empty(field=taxonomy_core.fields.System('post-editor-layout')),
                labels.SpecialEditorLayout: self._map_special_post_editor_layout,
                labels.ExcludedFromSearch: lambda _: taxonomy_core.labels.Badge(field=taxonomy_core.fields.System('post-is-excluded-from-search')),
            })

        def visit_label(self, label):
            return self.label_to_factory_func_map[type(label)](label)

        @staticmethod
        def _map_post_id(label: labels.Id) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-id'), value=label.value)

        def _map_post_type(self, label: labels.Type) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-type'), value=self.aspects.map_post_type(label.type))

        def _map_post_status(self, label: labels.Status) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-status'), value=self.aspects.map_post_status(label.status))

        @staticmethod
        def _map_primary_post_tag(label: labels.PrimaryTag) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-primary-tag'), value=label.slug)

        @staticmethod
        def _map_regular_post_tag(label: labels.RegularTag) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-regular-tag'), value=label.slug)

        @staticmethod
        def _map_primary_post_section(label: labels.PrimarySection) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-primary-section'), value=label.id)

        @staticmethod
        def _map_regular_post_section(label: labels.RegularSection) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-regular-section'), value=label.id)

        @staticmethod
        def _map_post_community(label: labels.Community) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-community'), value=label.id)

        @staticmethod
        def _map_post_author(label: labels.Author) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-author'), value=label.id)

        @staticmethod
        def _map_post_stage(label: labels.Stage) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-stage'), value=label.id)

        @staticmethod
        def _map_custom_post_field(label: labels.CustomField) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.Custom('post-custom-field', path=label.path), value=label.value)

        @staticmethod
        def _map_no_custom_post_field(label: labels.NoCustomField) -> taxonomy_core.labels.Empty:
            return taxonomy_core.labels.Empty(field=taxonomy_core.fields.Custom('post-custom-field', path=label.path))

        @staticmethod
        def _map_special_post_page_layout(label: labels.SpecialPageLayout) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-page-layout'), value=label.slug)

        @staticmethod
        def _map_special_post_editor_layout(label: labels.SpecialEditorLayout) -> taxonomy_core.labels.Value:
            return taxonomy_core.labels.Value(field=taxonomy_core.fields.System('post-editor-layout'), value=label.slug)


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
