from unittest.mock import Mock
from unittest.mock import call

from pytest import fixture

from rmshared.content.taxonomy.core.fakes import Fakes
from rmshared.content.taxonomy.core.traversal.abc import IFilters
from rmshared.content.taxonomy.core.traversal.abc import ILabels
from rmshared.content.taxonomy.core.traversal.abc import IRanges
from rmshared.content.taxonomy.core.traversal.abc import IEvents
from rmshared.content.taxonomy.core.traversal.composite import Composite


class TestComposite:
    @fixture
    def traverser(self, filters: IFilters, labels: ILabels, ranges: IRanges, events: IEvents) -> Composite:
        return Composite(filters=filters, labels=labels, ranges=ranges, events=events)

    @fixture
    def filters(self) -> IFilters | Mock:
        return Mock(spec=IFilters)

    @fixture
    def labels(self) -> ILabels | Mock:
        return Mock(spec=ILabels)

    @fixture
    def ranges(self) -> IRanges | Mock:
        return Mock(spec=IRanges)

    @fixture
    def events(self) -> IEvents | Mock:
        return Mock(spec=IEvents)

    @fixture
    def fakes(self):
        return Fakes()

    def test_filters(self, fakes: Fakes, traverser: Composite, filters: IFilters | Mock):
        filters_ = tuple(fakes.sample_filters(max_size=2, min_size=2))
        visitor = Mock()
        filters.traverse_filters = Mock()
        assert traverser.traverse_filters(filters_, visitor) is None
        assert filters.traverse_filters.call_args_list == [call(filters_, visitor)]

    def test_labels(self, fakes: Fakes, traverser: Composite, labels: ILabels | Mock):
        labels_ = tuple(fakes._sample_labels())
        visitor = Mock()
        labels.traverse_labels = Mock()
        assert traverser.traverse_labels(labels_, visitor) is None
        assert labels.traverse_labels.call_args_list == [call(labels_, visitor)]

    def test_ranges(self, fakes: Fakes, traverser: Composite, ranges: IRanges | Mock):
        ranges_ = tuple(fakes._sample_ranges())
        visitor = Mock()
        ranges.traverse_ranges = Mock()
        assert traverser.traverse_ranges(ranges_, visitor) is None
        assert ranges.traverse_ranges.call_args_list == [call(ranges_, visitor)]

    def test_events(self, fakes: Fakes, traverser: Composite, events: IEvents | Mock):
        events_ = tuple(fakes.sample_events(max_size=2, min_size=2))
        visitor = Mock()
        events.traverse_events = Mock()
        assert traverser.traverse_events(events_, visitor) is None
        assert events.traverse_events.call_args_list == [call(events_, visitor)]
