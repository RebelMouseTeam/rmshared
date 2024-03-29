from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core.protocols.abc import ILabels
from rmshared.content.taxonomy.core.protocols.abc import IRanges
from rmshared.content.taxonomy.core.protocols.ui.filters import Filters


class TestFilters:
    @fixture
    def protocol(self, labels_: ILabels, ranges_: IRanges) -> Filters:
        return Filters(labels=labels_, ranges=ranges_)

    @fixture
    def labels_(self) -> ILabels | Mock:
        return Mock(spec=ILabels)

    @fixture
    def ranges_(self) -> IRanges | Mock:
        return Mock(spec=IRanges)

    def test_any_label(self, protocol: Filters, labels_: ILabels | Mock):
        labels_.make_label = Mock(side_effect=['label_1', 'label_2'])
        labels_.jsonify_label = Mock(side_effect=[{'label_1': {}}, {'label_2': {}}])

        assert protocol.make_filter({'any_label': [{'label_1': {}}, {'label_2': {}}]}) == filters.AnyLabel(labels=('label_1', 'label_2'))
        assert protocol.jsonify_filter(filters.AnyLabel(labels=('label_1', 'label_2'))) == {'any_label': [{'label_1': {}}, {'label_2': {}}]}
        assert labels_.make_label.call_args_list == [call({'label_1': {}}), call({'label_2': {}})]
        assert labels_.jsonify_label.call_args_list == [call('label_1'), call('label_2')]

    def test_no_labels(self, protocol: Filters, labels_: ILabels):
        labels_.make_label = Mock(side_effect=['label_3', 'label_4'])
        labels_.jsonify_label = Mock(side_effect=[{'label_3': {}}, {'label_4': {}}])

        assert protocol.make_filter({'no_labels': [{'label_3': {}}, {'label_4': {}}]}) == filters.NoLabels(labels=('label_3', 'label_4'))
        assert protocol.jsonify_filter(filters.NoLabels(labels=('label_3', 'label_4'))) == {'no_labels': [{'label_3': {}}, {'label_4': {}}]}
        assert labels_.make_label.call_args_list == [call({'label_3': {}}), call({'label_4': {}})]
        assert labels_.jsonify_label.call_args_list == [call('label_3'), call('label_4')]

    def test_any_range(self, protocol: Filters, ranges_: IRanges | Mock):
        ranges_.make_range = Mock(side_effect=['range_1', 'range_2'])
        ranges_.jsonify_range = Mock(side_effect=[{'range_1': {}}, {'range_2': {}}])

        assert protocol.make_filter({'any_range': [{'range_1': {}}, {'range_2': {}}]}) == filters.AnyRange(ranges=('range_1', 'range_2'))
        assert protocol.jsonify_filter(filters.AnyRange(ranges=('range_1', 'range_2'))) == {'any_range': [{'range_1': {}}, {'range_2': {}}]}
        assert ranges_.make_range.call_args_list == [call({'range_1': {}}), call({'range_2': {}})]
        assert ranges_.jsonify_range.call_args_list == [call('range_1'), call('range_2')]

    def test_no_ranges(self, protocol: Filters, ranges_: IRanges):
        ranges_.make_range = Mock(side_effect=['range_3', 'range_4'])
        ranges_.jsonify_range = Mock(side_effect=[{'range_3': {}}, {'range_4': {}}])

        assert protocol.make_filter({'no_ranges': [{'range_3': {}}, {'range_4': {}}]}) == filters.NoRanges(ranges=('range_3', 'range_4'))
        assert protocol.jsonify_filter(filters.NoRanges(ranges=('range_3', 'range_4'))) == {'no_ranges': [{'range_3': {}}, {'range_4': {}}]}
        assert ranges_.make_range.call_args_list == [call({'range_3': {}}), call({'range_4': {}})]
        assert ranges_.jsonify_range.call_args_list == [call('range_3'), call('range_4')]
