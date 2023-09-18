from pytest import fixture

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import protocols


class TestProtocol:
    NOW = 1440000000

    @fixture
    def protocol(self) -> protocols.IComposite:
        return protocols.Factory.make_instance_for_ui().make_composite()

    def test_it_should_make_filters(self, protocol: protocols.IComposite):
        filters_ = tuple(map(protocol.make_filter, self.FILTERS_DATA))
        assert filters_ == self.FILTERS

    def test_it_should_jsonify_filters(self, protocol: protocols.IComposite):
        data = tuple(map(protocol.jsonify_filter, self.FILTERS))
        assert data == self.FILTERS_DATA

    FILTERS = tuple([
        filters.AnyLabel(labels=(
            labels.Value(field=fields.System('post-id'), value=123),
            labels.Value(field=fields.System('post-type'), value='how-to'),
            labels.Value(field=fields.System('post-status'), value='published-to-community(demoted=true)'),
        )),
        filters.NoLabels(labels=(
            labels.Badge(field=fields.System('private-post')),
            labels.Empty(field=fields.Custom('custom-post-field', path='path.to.field')),
        )),
        filters.AnyRange(ranges=(
            ranges.Between(field=fields.System('post-modified-at'), min_value=NOW - 100, max_value=NOW + 100),
        )),
        filters.NoRanges(ranges=(
            ranges.MoreThan(field=fields.System('post-scheduled-at'), value=NOW - 200),
            ranges.LessThan(field=fields.System('post-published-at'), value=NOW + 300),
        )),
    ])

    FILTERS_DATA = tuple([
        {'any_label': [
            {'value': {'field': {'post-id': {}}, 'value': 123}},
            {'value': {'field': {'post-type': {}}, 'value': 'how-to'}},
            {'value': {'field': {'post-status': {}}, 'value': 'published-to-community(demoted=true)'}},
        ]},
        {'no_labels': [
            {'badge': {'field': {'private-post': {}}}},
            {'empty': {'field': {'custom-post-field': {'path': 'path.to.field'}}}},
        ]},
        {'any_range': [
            {'field': {'post-modified-at': {}}, 'min': NOW - 100, 'max': NOW + 100},
        ]},
        {'no_ranges': [
            {'field': {'post-scheduled-at': {}}, 'min': NOW - 200},
            {'field': {'post-published-at': {}}, 'max': NOW + 300},
        ]},
    ])
