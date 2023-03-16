from pytest import fixture

from rmshared.content.taxonomy import protocols as taxonomy_protocols
from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import orders
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import protocol


class TestServerProtocol:
    NOW = 1440000000

    @fixture
    def protocol_(self) -> taxonomy_protocols.IProtocol:
        return protocol.Factory().make_protocol()

    def test_it_should_make_filters(self, protocol_: taxonomy_protocols.IProtocol):
        filters_ = tuple(protocol_.make_filters(data=self.FILTERS_DATA))
        assert filters_ == self.FILTERS

    def test_it_should_jsonify_filters(self, protocol_: taxonomy_protocols.IProtocol):
        data = tuple(protocol_.jsonify_filters(filters_=self.FILTERS))
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

    def test_it_should_make_order(self, protocol_: taxonomy_protocols.IProtocol):
        order = protocol_.make_order(data={'value': {
            'field': {'post-modified-at': {}},
            'reverse': False,
        }})
        assert order == orders.Value(field=fields.System('post-modified-at'), reverse=False)
