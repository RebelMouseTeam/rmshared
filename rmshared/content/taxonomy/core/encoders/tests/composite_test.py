from unittest.mock import Mock
from unittest.mock import call

from pytest import fixture

from rmshared.content.taxonomy.core.encoders import IFilters
from rmshared.content.taxonomy.core.encoders import ILabels
from rmshared.content.taxonomy.core.encoders import IRanges
from rmshared.content.taxonomy.core.encoders import IFields
from rmshared.content.taxonomy.core.encoders import IEvents
from rmshared.content.taxonomy.core.encoders import IValues
from rmshared.content.taxonomy.core.encoders.composite import Composite


class TestComposite:
    @fixture
    def encoder(self, filters: IFilters, labels: ILabels, ranges: IRanges, fields: IFields, events: IEvents, values: IValues) -> Composite:
        return Composite(filters=filters, labels=labels, ranges=ranges, fields=fields, events=events, values=values)

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
    def fields(self) -> IFields | Mock:
        return Mock(spec=IFields)

    @fixture
    def events(self) -> IEvents | Mock:
        return Mock(spec=IEvents)

    @fixture
    def values(self) -> IValues | Mock:
        return Mock(spec=IValues)

    def test_filters(self, encoder: Composite, filters: IFilters | Mock):
        filter_ = object()
        filters.encode_filter = Mock(return_value={'filter': {}})
        assert encoder.encode_filter(filter_) == {'filter': {}}
        assert filters.encode_filter.call_args_list == [call(filter_)]

    def test_labels(self, encoder: Composite, labels: ILabels | Mock):
        label = object()
        labels.encode_label = Mock(return_value={'label': {}})
        assert encoder.encode_label(label) == {'label': {}}
        assert labels.encode_label.call_args_list == [call(label)]

    def test_ranges(self, encoder: Composite, ranges: IRanges | Mock):
        range_ = object()
        ranges.encode_range = Mock(return_value={'range': {}})
        assert encoder.encode_range(range_) == {'range': {}}
        assert ranges.encode_range.call_args_list == [call(range_)]

    def test_fields(self, encoder: Composite, fields: IFields | Mock):
        field = object()
        fields.encode_field = Mock(return_value={'field': {}})
        assert encoder.encode_field(field) == {'field': {}}
        assert fields.encode_field.call_args_list == [call(field)]

    def test_events(self, encoder: Composite, events: IEvents | Mock):
        event = object()
        events.encode_event = Mock(return_value={'event': {}})
        assert encoder.encode_event(event) == {'event': {}}
        assert events.encode_event.call_args_list == [call(event)]

    def test_values(self, encoder: Composite, values: IValues | Mock):
        value = object()
        values.encode_value = Mock(return_value={'value': {}})
        assert encoder.encode_value(value) == {'value': {}}
        assert values.encode_value.call_args_list == [call(value)]
