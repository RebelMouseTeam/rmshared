from unittest.mock import Mock
from unittest.mock import call

from pytest import fixture

from rmshared.content.taxonomy.core.protocols.abc import IBuilder
from rmshared.content.taxonomy.core.protocols.abc import IFilters
from rmshared.content.taxonomy.core.protocols.abc import ILabels
from rmshared.content.taxonomy.core.protocols.abc import IRanges
from rmshared.content.taxonomy.core.protocols.abc import IFields
from rmshared.content.taxonomy.core.protocols.abc import IEvents
from rmshared.content.taxonomy.core.protocols.abc import IValues
from rmshared.content.taxonomy.core.protocols.factory import Factory
from rmshared.content.taxonomy.core.protocols.composite import Composite


class TestFactory:
    @fixture
    def factory(self, builder: IBuilder) -> Factory:
        return Factory(builder)

    @fixture
    def builder(self) -> IBuilder | Mock:
        return Mock(spec=IBuilder)

    def test_it_should_create_composite(self, factory: Factory, builder: IBuilder | Mock):
        filters = Mock(spec=IFilters)
        labels = Mock(spec=ILabels)
        ranges = Mock(spec=IRanges)
        fields = Mock(spec=IFields)
        events = Mock(spec=IEvents)
        values = Mock(spec=IValues)

        builder.make_filters = Mock(return_value=filters)
        builder.make_labels = Mock(return_value=labels)
        builder.make_ranges = Mock(return_value=ranges)
        builder.make_fields = Mock(return_value=fields)
        builder.make_events = Mock(return_value=events)
        builder.make_values = Mock(return_value=values)

        composite = factory.make_composite()

        assert isinstance(composite, Composite)
        assert composite.filters == filters
        assert composite.labels == labels
        assert composite.ranges == ranges
        assert composite.fields == fields
        assert composite.events == events
        assert composite.values == values
        assert builder.make_filters.call_args_list == [call(labels, ranges)]
        assert builder.make_labels.call_args_list == [call(fields, values)]
        assert builder.make_ranges.call_args_list == [call(fields, values)]
        assert builder.make_fields.call_args_list == [call()]
        assert builder.make_events.call_args_list == [call()]
        assert builder.make_values.call_args_list == [call()]
