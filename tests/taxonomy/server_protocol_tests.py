from pytest import fixture

from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import filters
from rmshared.content.taxonomy.abc import Range
from rmshared.content.taxonomy.server import Protocol


class TestServerProtocol:
    NOW = 1440000000

    @fixture
    def protocol(self) -> Protocol:
        return Protocol()

    def test_it_should_parse_post_filters(self, protocol: Protocol):
        filters_ = protocol.filters.make_filters(data=[
            {'any_label': [
                {'post-id': 123},
                {'post-type': {'how-to': {}}},
                {'post-status': {'published': {'scope': {'community': {'is_demoted': True}}}}},
            ]},
            {'no_labels': [
                {'private-post': {}},
                {'suspicious-post': {}},
            ]},
            {'any_label': [
                {'post-primary-tag': {'slug': 'primary-tag'}},
                {'post-regular-tag': {'slug': 'regular-tag'}},
                {'post-primary-section': {'id': 123}},
                {'post-regular-section': {'id': 456}},
                {'post-community': {'id': 789}},
                {'post-author': {'id': 890}},
                {'post-stage': {'id': 901}},
                {'post-custom-field': {'path': 'path.to.value', 'value': 'some-value'}},
                {'special-post-page-layout': {'slug': 'some-post-page-layout'}},
                {'special-post-editor-layout': {'slug': 'some-post-editor-layout'}},
            ]},
            {'no_labels': [
                {'post-without-primary-tags': {}},
                {'post-without-regular-tags': {}},
                {'post-without-primary-sections': {}},
                {'post-without-regular-sections': {}},
                {'post-without-communities': {}},
                {'post-without-authors': {}},
                {'post-without-stages': {}},
                {'post-without-custom-field': {'path': 'path.to.value'}},
                {'default-post-page-layout': {}},
                {'default-post-editor-layout': {}},
            ]},
            {'any_range': [
                {'field': {'post-modified-at': {}}, 'min': self.NOW - 100, 'max': self.NOW + 100},
            ]},
            {'no_ranges': [
                {'field': {'post-scheduled-at': {}}, 'min': self.NOW - 200, 'max': self.NOW + 200},
                {'field': {'post-published-at': {}}, 'min': self.NOW - 300, 'max': self.NOW + 300},
            ]},
            {'any_range': [
                {'field': {'lifetime-post-page-views': {}}, 'min': 1234, 'max': 4567},
            ]},
            {'no_ranges': [
                {'field': {'custom-post-field': {'path': 'path.to.value'}}, 'min': 'A', 'max': 'Z'},
            ]},
            {'phrase': {'phrase': 'Hello'}},
            {'phrase': {'phrase': 'World', 'weights': ['10', '0', '4']}},
        ])
        assert filters_ == frozenset({
            filters.AnyLabel(labels=(
                posts.labels.Id(value=123),
                posts.labels.Type(type=posts.consts.POST.TYPE.HOW_TO),
                posts.labels.Status(status=posts.statuses.Published(
                    scope=posts.published.scopes.Community(is_demoted=True)
                )),
            )),
            filters.NoLabels(labels=(
                posts.labels.Private(),
                posts.labels.Suspicious(),
            )),
            filters.AnyLabel(labels=(
                posts.labels.PrimaryTag(slug='primary-tag'),
                posts.labels.RegularTag(slug='regular-tag'),
                posts.labels.PrimarySection(id=123),
                posts.labels.RegularSection(id=456),
                posts.labels.Community(id=789),
                posts.labels.Author(id=890),
                posts.labels.Stage(id=901),
                posts.labels.CustomField(path='path.to.value', value='some-value'),
                posts.labels.SpecialPageLayout(slug='some-post-page-layout'),
                posts.labels.SpecialEditorLayout(slug='some-post-editor-layout'),
            )),
            filters.NoLabels(labels=(
                posts.labels.NoPrimaryTags(),
                posts.labels.NoRegularTags(),
                posts.labels.NoPrimarySections(),
                posts.labels.NoRegularSections(),
                posts.labels.NoCommunities(),
                posts.labels.NoAuthors(),
                posts.labels.NoStages(),
                posts.labels.NoCustomField(path='path.to.value'),
                posts.labels.DefaultPageLayout(),
                posts.labels.DefaultEditorLayout(),
            )),
            filters.AnyRange(ranges=(
                Range(
                    field=posts.fields.ModifiedAt(),
                    min_value=self.NOW - 100,
                    max_value=self.NOW + 100,
                ),
            )),
            filters.NoRanges(ranges=(
                Range(
                    field=posts.fields.ScheduledAt(),
                    min_value=self.NOW - 200,
                    max_value=self.NOW + 200,
                ),
                Range(
                    field=posts.fields.PublishedAt(),
                    min_value=self.NOW - 300,
                    max_value=self.NOW + 300,
                ),
            )),
            filters.AnyRange(ranges=(
                Range(
                    field=posts.fields.LifetimePageViews(),
                    min_value=1234,
                    max_value=4567,
                ),
            )),
            filters.NoRanges(ranges=(
                Range(
                    field=posts.fields.CustomField(path='path.to.value'),
                    min_value='A',
                    max_value='Z',
                ),
            )),
            filters.Phrase(phrase='Hello', weights=None),
            filters.Phrase(phrase='World', weights=(10, 0, 4)),
        })
