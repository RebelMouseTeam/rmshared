from pytest import fixture

from rmshared.content.taxonomy.core0 import fields
from rmshared.content.taxonomy.core0 import labels
from rmshared.content.taxonomy.core0 import orders
from rmshared.content.taxonomy.core0 import ranges
from rmshared.content.taxonomy.core0 import filters
from rmshared.content.taxonomy.core0.server.protocol import Protocol


class TestServerProtocol:
    NOW = 1440000000

    @fixture
    def protocol(self) -> Protocol:
        return Protocol()

    def test_it_should_make_filters(self, protocol: Protocol):
        filters_ = tuple(protocol.make_filters(data=self.FILTERS_DATA))
        assert filters_ == self.FILTERS

    def test_it_should_jsonify_filters(self, protocol: Protocol):
        data = tuple(protocol.jsonify_filters(filters=self.FILTERS))
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

    def test_it_should_make_order(self, protocol: Protocol):
        order = protocol.make_order(data={
            'field': {'post-modified-at': {}},
            'reverse': False,
        })
        assert order == orders.Value(field=fields.System('post-modified-at'), reverse=False)
