from unittest.mock import Mock
from unittest.mock import call

from pytest import fixture

from rmshared.content.taxonomy.core.protocols import IFilters
from rmshared.content.taxonomy.core.protocols import ILabels
from rmshared.content.taxonomy.core.protocols import IRanges
from rmshared.content.taxonomy.core.protocols import IFields
from rmshared.content.taxonomy.core.protocols import IEvents
from rmshared.content.taxonomy.core.protocols import IValues
from rmshared.content.taxonomy.core.protocols.composite import Composite


class TestComposite:
    @fixture
    def protocol(self, filters: IFilters, labels: ILabels, ranges: IRanges, fields: IFields, events: IEvents, values: IValues) -> Composite:
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

    def test_filters(self, protocol: Composite, filters: IFilters | Mock):
        filter_ = object()
        filters.make_filter = Mock(return_value=filter_)
        filters.jsonify_filter = Mock(return_value={'filter': {}})
        assert protocol.make_filter(data={'filter': {}}) == filter_
        assert protocol.jsonify_filter(filter_) == {'filter': {}}
        assert filters.make_filter.call_args_list == [call({'filter': {}})]
        assert filters.jsonify_filter.call_args_list == [call(filter_)]

    def test_labels(self, protocol: Composite, labels: ILabels | Mock):
        label = object()
        labels.make_label = Mock(return_value=label)
        labels.jsonify_label = Mock(return_value={'label': {}})
        assert protocol.make_label(data={'label': {}}) == label
        assert protocol.jsonify_label(label) == {'label': {}}
        assert labels.make_label.call_args_list == [call({'label': {}})]
        assert labels.jsonify_label.call_args_list == [call(label)]

    def test_ranges(self, protocol: Composite, ranges: IRanges | Mock):
        range_ = object()
        ranges.make_range = Mock(return_value=range_)
        ranges.jsonify_range = Mock(return_value={'range': {}})
        assert protocol.make_range(data={'range': {}}) == range_
        assert protocol.jsonify_range(range_) == {'range': {}}
        assert ranges.make_range.call_args_list == [call({'range': {}})]
        assert ranges.jsonify_range.call_args_list == [call(range_)]

    def test_fields(self, protocol: Composite, fields: IFields | Mock):
        field = object()
        fields.make_field = Mock(return_value=field)
        fields.jsonify_field = Mock(return_value={'field': {}})
        assert protocol.make_field(data={'field': {}}) == field
        assert protocol.jsonify_field(field) == {'field': {}}
        assert fields.make_field.call_args_list == [call({'field': {}})]
        assert fields.jsonify_field.call_args_list == [call(field)]

    def test_events(self, protocol: Composite, events: IEvents | Mock):
        event = object()
        events.make_event = Mock(return_value=event)
        events.jsonify_event = Mock(return_value={'event': {}})
        assert protocol.make_event(data={'event': {}}) == event
        assert protocol.jsonify_event(event) == {'event': {}}
        assert events.make_event.call_args_list == [call({'event': {}})]
        assert events.jsonify_event.call_args_list == [call(event)]

    def test_values(self, protocol: Composite, values: IValues | Mock):
        value = object()
        values.make_value = Mock(return_value=value)
        values.jsonify_value = Mock(return_value={'value': {}})
        assert protocol.make_value(data={'value': {}}) == value
        assert protocol.jsonify_value(value) == {'value': {}}
        assert values.make_value.call_args_list == [call({'value': {}})]
        assert values.jsonify_value.call_args_list == [call(value)]
