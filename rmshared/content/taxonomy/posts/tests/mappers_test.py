from pytest import fixture

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.posts import labels
from rmshared.content.taxonomy.posts import fields
from rmshared.content.taxonomy.posts import consts
from rmshared.content.taxonomy.posts import statuses
from rmshared.content.taxonomy.posts import drafts
from rmshared.content.taxonomy.posts import published
from rmshared.content.taxonomy.posts import mappers


class TestMappers:
    @fixture
    def factory(self) -> mappers.Factory:
        return mappers.Factory()

    def test_it_should_map_filters(self, factory: mappers.Factory):
        visitor = factory.make_visitor()
        assert tuple(visitor.visit_filters(self.POSTS_FILTERS)) == tuple(self.CORE_FILTERS)

    POSTS_FILTERS = [
        core.filters.AnyLabel[labels.Base](labels=(
            labels.Id(value=123),
            labels.Status(status=statuses.Draft(stage=drafts.stages.Created(is_imported=True))),
            labels.Status(status=statuses.Draft(stage=drafts.stages.Created(is_imported=False))),
            labels.Status(status=statuses.Draft(stage=drafts.stages.InProgress(is_rejected=True))),
            labels.Status(status=statuses.Draft(stage=drafts.stages.InProgress(is_rejected=False))),
            labels.Status(status=statuses.Draft(stage=drafts.stages.InReview())),
            labels.Status(status=statuses.Draft(stage=drafts.stages.Ready())),
            labels.Suspicious(),
            labels.NoPrimaryTags(),
            labels.NoRegularTags(),
            labels.PrimarySection(id=234),
            labels.RegularSection(id=345),
            labels.NoCommunities(),
            labels.Author(id=456),
            labels.NoStages(),
            labels.CustomField(path='path.to.field_1', value='value-1'),
            labels.DefaultPageLayout(),
            labels.SpecialEditorLayout(slug='layout-1'),
        )),
        core.filters.NoLabels[labels.Base](labels=(
            labels.Type(type=consts.POST.TYPE.HOW_TO),
            labels.Status(status=statuses.Published(scope=published.scopes.Site(is_promoted=True))),
            labels.Status(status=statuses.Published(scope=published.scopes.Site(is_promoted=False))),
            labels.Status(status=statuses.Published(scope=published.scopes.Community(is_demoted=True))),
            labels.Status(status=statuses.Published(scope=published.scopes.Community(is_demoted=False))),
            labels.Status(status=statuses.Removed()),
            labels.Private(),
            labels.PrimaryTag(slug='tag-1'),
            labels.RegularTag(slug='tag-2'),
            labels.NoPrimarySections(),
            labels.NoRegularSections(),
            labels.Community(id=567),
            labels.NoAuthors(),
            labels.Stage(id=678),
            labels.NoCustomField(path='path.to.field_2'),
            labels.SpecialPageLayout(slug='layout-2'),
            labels.DefaultEditorLayout(),
            labels.ExcludedFromSearch(),
        )),
        core.filters.AnyRange[core.ranges.Range[fields.Base]](ranges=(
            core.ranges.Between(field=fields.ModifiedAt(), min_value=100, max_value=500),
            core.ranges.LessThan(field=fields.ScheduledAt(), value=300),
        )),
        core.filters.NoRanges[core.ranges.Range[fields.Base]](ranges=(
            core.ranges.MoreThan(field=fields.PublishedAt(), value=400),
            core.ranges.Between(field=fields.CustomField(path='path.to.field_3'), min_value=600, max_value=700),
        )),
    ]
    CORE_FILTERS = [
        core.filters.AnyLabel[core.labels.Label](labels=(
            core.labels.Value(field=core.fields.System(name='post-id'), value=123),
            core.labels.Value(field=core.fields.System(name='post-status'), value='draft-created(imported=true)'),
            core.labels.Value(field=core.fields.System(name='post-status'), value='draft-created(imported=false)'),
            core.labels.Value(field=core.fields.System(name='post-status'), value='draft-in-progress(rejected=true)'),
            core.labels.Value(field=core.fields.System(name='post-status'), value='draft-in-progress(rejected=false)'),
            core.labels.Value(field=core.fields.System(name='post-status'), value='draft-in-review'),
            core.labels.Value(field=core.fields.System(name='post-status'), value='draft-ready'),
            core.labels.Badge(field=core.fields.System(name='post-is-suspicious')),
            core.labels.Empty(field=core.fields.System(name='post-primary-tag')),
            core.labels.Empty(field=core.fields.System(name='post-regular-tag')),
            core.labels.Value(field=core.fields.System(name='post-primary-section'), value=234),
            core.labels.Value(field=core.fields.System(name='post-regular-section'), value=345),
            core.labels.Empty(field=core.fields.System(name='post-community')),
            core.labels.Value(field=core.fields.System(name='post-author'), value=456),
            core.labels.Empty(field=core.fields.System(name='post-stage')),
            core.labels.Value(field=core.fields.Custom(name='post-custom-field', path='path.to.field_1'), value='value-1'),
            core.labels.Empty(field=core.fields.System(name='post-page-layout')),
            core.labels.Value(field=core.fields.System(name='post-editor-layout'), value='layout-1'),
        )),
        core.filters.NoLabels[core.labels.Label](labels=(
            core.labels.Value(field=core.fields.System(name='post-type'), value='how-to'),
            core.labels.Value(field=core.fields.System(name='post-status'), value='published-to-site(promoted=true)'),
            core.labels.Value(field=core.fields.System(name='post-status'), value='published-to-site(promoted=false)'),
            core.labels.Value(field=core.fields.System(name='post-status'), value='published-to-community(demoted=true)'),
            core.labels.Value(field=core.fields.System(name='post-status'), value='published-to-community(demoted=false)'),
            core.labels.Value(field=core.fields.System(name='post-status'), value='removed'),
            core.labels.Badge(field=core.fields.System(name='post-is-private')),
            core.labels.Value(field=core.fields.System(name='post-primary-tag'), value='tag-1'),
            core.labels.Value(field=core.fields.System(name='post-regular-tag'), value='tag-2'),
            core.labels.Empty(field=core.fields.System(name='post-primary-section')),
            core.labels.Empty(field=core.fields.System(name='post-regular-section')),
            core.labels.Value(field=core.fields.System(name='post-community'), value=567),
            core.labels.Empty(field=core.fields.System(name='post-author')),
            core.labels.Value(field=core.fields.System(name='post-stage'), value=678),
            core.labels.Empty(field=core.fields.Custom(name='post-custom-field', path='path.to.field_2')),
            core.labels.Value(field=core.fields.System(name='post-page-layout'), value='layout-2'),
            core.labels.Empty(field=core.fields.System(name='post-editor-layout')),
            core.labels.Badge(field=core.fields.System(name='post-is-excluded-from-search')),
        )),
        core.filters.AnyRange[core.ranges.Range](ranges=(
            core.ranges.Between(field=core.fields.System(name='post-modified-at'), min_value=100, max_value=500),
            core.ranges.LessThan(field=core.fields.System(name='post-scheduled-at'), value=300),
        )),
        core.filters.NoRanges[core.ranges.Range](ranges=(
            core.ranges.MoreThan(field=core.fields.System(name='post-published-at'), value=400),
            core.ranges.Between(field=core.fields.Custom(name='post-custom-field', path='path.to.field_3'), min_value=600, max_value=700),
        )),
    ]
