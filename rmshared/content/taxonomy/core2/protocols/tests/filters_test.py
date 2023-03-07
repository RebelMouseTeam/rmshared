from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core2 import filters
from rmshared.content.taxonomy.core2.protocols.abc import ILabels
from rmshared.content.taxonomy.core2.protocols.abc import IRanges
from rmshared.content.taxonomy.core2.protocols.filters import Filters


class TestFilters:
    @fixture
    def filters_(self, labels_: ILabels, ranges_: IRanges) -> Filters:
        return Filters(labels_, ranges_)

    @fixture
    def labels_(self) -> ILabels | Mock:
        return Mock(spec=ILabels)

    @fixture
    def ranges_(self) -> IRanges | Mock:
        return Mock(spec=IRanges)

    def test_it_should_make_filter(self, filters_, labels_: ILabels, ranges_: IRanges):
        labels_.make_label = Mock(side_effect=['label_1', 'label_2', 'label_3', 'label_4'])
        ranges_.make_range = Mock(side_effect=['range_1', 'range_2', 'range_3', 'range_4'])

        assert filters_.make_filter({'any_label': [{'label_1': {}}, {'label_2': {}}]}) == filters.AnyLabel(labels=('label_1', 'label_2'))
        assert filters_.make_filter({'no_labels': [{'label_3': {}}, {'label_4': {}}]}) == filters.NoLabels(labels=('label_3', 'label_4'))
        assert filters_.make_filter({'any_range': [{'range_1': {}}, {'range_2': {}}]}) == filters.AnyRange(ranges=('range_1', 'range_2'))
        assert filters_.make_filter({'no_ranges': [{'range_3': {}}, {'range_4': {}}]}) == filters.NoRanges(ranges=('range_3', 'range_4'))
        assert labels_.make_label.call_args_list == [
            call({'label_1': {}}),
            call({'label_2': {}}),
            call({'label_3': {}}),
            call({'label_4': {}}),
        ]
        assert ranges_.make_range.call_args_list == [
            call({'range_1': {}}),
            call({'range_2': {}}),
            call({'range_3': {}}),
            call({'range_4': {}}),
        ]

    def test_it_should_jsonify_filter(self, filters_, labels_: ILabels, ranges_: IRanges):
        labels_.jsonify_label = Mock(side_effect=[{'label_1': {}}, {'label_2': {}}, {'label_3': {}}, {'label_4': {}}])
        ranges_.jsonify_range = Mock(side_effect=[{'range_1': {}}, {'range_2': {}}, {'range_3': {}}, {'range_4': {}}])

        assert filters_.jsonify_filter(filters.AnyLabel(labels=('label_1', 'label_2'))) == {'any_label': [{'label_1': {}}, {'label_2': {}}]}
        assert filters_.jsonify_filter(filters.NoLabels(labels=('label_3', 'label_4'))) == {'no_labels': [{'label_3': {}}, {'label_4': {}}]}
        assert filters_.jsonify_filter(filters.AnyRange(ranges=('range_1', 'range_2'))) == {'any_range': [{'range_1': {}}, {'range_2': {}}]}
        assert filters_.jsonify_filter(filters.NoRanges(ranges=('range_3', 'range_4'))) == {'no_ranges': [{'range_3': {}}, {'range_4': {}}]}
        assert labels_.jsonify_label.call_args_list == [
            call('label_1'),
            call('label_2'),
            call('label_3'),
            call('label_4'),
        ]
        assert ranges_.jsonify_range.call_args_list == [
            call('range_1'),
            call('range_2'),
            call('range_3'),
            call('range_4'),
        ]
