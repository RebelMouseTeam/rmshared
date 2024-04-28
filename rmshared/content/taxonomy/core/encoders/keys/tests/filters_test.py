from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core.encoders.abc import ILabels
from rmshared.content.taxonomy.core.encoders.abc import IRanges
from rmshared.content.taxonomy.core.encoders.keys.filters import Filters


class TestFilters:
    @fixture
    def encoder(self, labels_: ILabels, ranges_: IRanges) -> Filters:
        return Filters(labels=labels_, ranges=ranges_)

    @fixture
    def labels_(self) -> ILabels | Mock:
        return Mock(spec=ILabels)

    @fixture
    def ranges_(self) -> IRanges | Mock:
        return Mock(spec=IRanges)

    def test_any_label(self, encoder: Filters, labels_: ILabels | Mock):
        labels_.encode_label = Mock(side_effect=['l_1', 'l_2'])
        assert encoder.encode_filter(filters.AnyLabel(labels=('label_1', 'label_2'))) == '+l(l_1,l_2)'
        assert labels_.encode_label.call_args_list == [call('label_1'), call('label_2')]
        labels_.encode_label = Mock(side_effect=['l_2', 'l_1'])
        assert encoder.encode_filter(filters.AnyLabel(labels=('label_2', 'label_1'))) == '+l(l_1,l_2)'
        assert labels_.encode_label.call_args_list == [call('label_2'), call('label_1')]

    def test_no_labels(self, encoder: Filters, labels_: ILabels):
        labels_.encode_label = Mock(side_effect=['l_3', 'l_4'])
        assert encoder.encode_filter(filters.NoLabels(labels=('label_3', 'label_4'))) == '-l(l_3,l_4)'
        assert labels_.encode_label.call_args_list == [call('label_3'), call('label_4')]
        labels_.encode_label = Mock(side_effect=['l_4', 'l_3'])
        assert encoder.encode_filter(filters.NoLabels(labels=('label_4', 'label_3'))) == '-l(l_3,l_4)'
        assert labels_.encode_label.call_args_list == [call('label_4'), call('label_3')]

    def test_any_range(self, encoder: Filters, ranges_: IRanges | Mock):
        ranges_.encode_range = Mock(side_effect=['r_1', 'r_2'])
        assert encoder.encode_filter(filters.AnyRange(ranges=('range_1', 'range_2'))) == '+r(r_1,r_2)'
        assert ranges_.encode_range.call_args_list == [call('range_1'), call('range_2')]
        ranges_.encode_range = Mock(side_effect=['r_2', 'r_1'])
        assert encoder.encode_filter(filters.AnyRange(ranges=('range_2', 'range_1'))) == '+r(r_1,r_2)'
        assert ranges_.encode_range.call_args_list == [call('range_2'), call('range_1')]

    def test_no_ranges(self, encoder: Filters, ranges_: IRanges):
        ranges_.encode_range = Mock(side_effect=['r_3', 'r_4'])
        assert encoder.encode_filter(filters.NoRanges(ranges=('range_3', 'range_4'))) == '-r(r_3,r_4)'
        assert ranges_.encode_range.call_args_list == [call('range_3'), call('range_4')]
        ranges_.encode_range = Mock(side_effect=['r_4', 'r_3'])
        assert encoder.encode_filter(filters.NoRanges(ranges=('range_4', 'range_3'))) == '-r(r_3,r_4)'
        assert ranges_.encode_range.call_args_list == [call('range_4'), call('range_3')]
