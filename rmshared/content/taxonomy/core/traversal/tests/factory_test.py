from unittest.mock import Mock
from unittest.mock import call

from pytest import fixture

from rmshared.content.taxonomy.core.traversal.abc import IAssembler
from rmshared.content.taxonomy.core.traversal.abc import IFilters
from rmshared.content.taxonomy.core.traversal.abc import ILabels
from rmshared.content.taxonomy.core.traversal.abc import IRanges
from rmshared.content.taxonomy.core.traversal.abc import IEvents
from rmshared.content.taxonomy.core.traversal.factory import Factory
from rmshared.content.taxonomy.core.traversal.composite import Composite


class TestFactory:
    @fixture
    def factory(self, assembler: IAssembler) -> Factory:
        return Factory(assembler)

    @fixture
    def assembler(self) -> IAssembler | Mock:
        return Mock(spec=IAssembler)

    def test_it_should_make_composite(self, factory: Factory, assembler: IAssembler | Mock):
        filters = Mock(spec=IFilters)
        labels = Mock(spec=ILabels)
        ranges = Mock(spec=IRanges)
        events = Mock(spec=IEvents)

        assembler.make_filters = Mock(return_value=filters)
        assembler.make_labels = Mock(return_value=labels)
        assembler.make_ranges = Mock(return_value=ranges)
        assembler.make_events = Mock(return_value=events)

        composite = factory.make_composite()

        assert isinstance(composite, Composite)
        assert composite.filters == filters
        assert composite.labels == labels
        assert composite.ranges == ranges
        assert composite.events == events
        assert assembler.make_filters.call_args_list == [call(labels, ranges)]
        assert assembler.make_labels.call_args_list == [call()]
        assert assembler.make_ranges.call_args_list == [call()]
        assert assembler.make_events.call_args_list == [call()]
