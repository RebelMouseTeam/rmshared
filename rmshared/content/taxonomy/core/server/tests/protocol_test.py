from pytest import fixture

from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import orders
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core.abc import Field
from rmshared.content.taxonomy.core.server.protocol import Protocol


class TestServerProtocol:
    NOW = 1440000000

    @fixture
    def protocol(self) -> Protocol:
        return Protocol()

    def test_it_should_parse_filters(self, protocol: Protocol):
        filters_ = frozenset(protocol.make_filters(data=[
            {'any_label': [
                {'value': {'field': {'post-id': {}}, 'value': 123}},
                {'value': {'field': {'post-type': {}}, 'value': 'how-to'}},
                {'value': {'field': {'post-status': {}}, 'value': 'published-to-community(demoted=true)'}},
            ]},
            {'no_labels': [
                {'badge': {'field': {'private-post': {}}}},
                {'empty': {'field': {'custom-post-field(path.to.field)': {}}}},
            ]},
            {'any_range': [
                {'field': {'post-modified-at': {}}, 'min': self.NOW - 100, 'max': self.NOW + 100},
            ]},
            {'no_ranges': [
                {'field': {'post-scheduled-at': {}}, 'min': self.NOW - 200, 'max': None},
                {'field': {'post-published-at': {}}, 'min': None, 'max': self.NOW + 300},
            ]},
        ]))
        assert filters_ == frozenset({
            filters.AnyLabel(labels=(
                labels.Value(field=Field('post-id'), value=123),
                labels.Value(field=Field('post-type'), value='how-to'),
                labels.Value(field=Field('post-status'), value='published-to-community(demoted=true)'),
            )),
            filters.NoLabels(labels=(
                labels.Badge(field=Field('private-post')),
                labels.Empty(field=Field('custom-post-field(path.to.field)')),
            )),
            filters.AnyRange(ranges=(
                ranges.Between(field=Field('post-modified-at'), min_value=self.NOW - 100, max_value=self.NOW + 100),
            )),
            filters.NoRanges(ranges=(
                ranges.MoreThan(field=Field('post-scheduled-at'), value=self.NOW - 200),
                ranges.LessThan(field=Field('post-published-at'), value=self.NOW + 300),
            )),
        })

    def test_it_should_parse_order(self, protocol: Protocol):
        order = protocol.make_order(data={
            'field': {'post-modified-at': {}},
            'reverse': False,
        })
        assert order == orders.Value(field=Field('post-modified-at'), reverse=False)
