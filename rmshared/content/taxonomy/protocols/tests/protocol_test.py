from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.protocols.abc import IFilters
from rmshared.content.taxonomy.protocols.abc import IOrders
from rmshared.content.taxonomy.protocols.abc import IFields
from rmshared.content.taxonomy.protocols.protocol import Protocol


class TestProtocol:
    @fixture
    def protocol(self, filters: IFilters, orders: IOrders, fields: IFields) -> Protocol:
        return Protocol(filters, orders, fields)

    @fixture
    def filters(self) -> IFilters | Mock:
        return Mock(spec=IFilters)

    @fixture
    def orders(self) -> IOrders | Mock:
        return Mock(spec=IOrders)

    @fixture
    def fields(self) -> IFields | Mock:
        return Mock(spec=IFields)

    def test_it_should_make_filters(self, protocol: Protocol, filters: IFilters | Mock):
        filter_1 = object()
        filter_2 = object()

        filters.make_filter = Mock(side_effect=[filter_1, filter_2])

        data = [{'filter_1': {'some': 'here'}}, {'filter2': {}}]
        assert list(protocol.make_filters(data)) == [filter_1, filter_2]
        assert filters.make_filter.call_args_list == [
            call({'filter_1': {'some': 'here'}}),
            call({'filter2': {}}),
        ]

    def test_it_should_jsonify_filters(self, protocol: Protocol, filters: IFilters | Mock):
        filters.jsonify_filter = Mock(side_effect=[{'filter_1': {'some': 'here'}}, {'filter2': {}}])

        filter_1 = object()
        filter_2 = object()
        assert protocol.jsonify_filters([filter_1, filter_2]) == [{'filter_1': {'some': 'here'}}, {'filter2': {}}]
        assert filters.jsonify_filter.call_args_list == [
            call(filter_1),
            call(filter_2),
        ]

    def test_it_should_make_orders(self, protocol: Protocol, orders: IOrders | Mock):
        order_1 = object()
        order_2 = object()

        orders.make_order = Mock(side_effect=[order_1, order_2])

        assert protocol.make_order({'order_1': {'some': 'here'}}) == order_1
        assert protocol.make_order({'order2': {}}) == order_2
        assert orders.make_order.call_args_list == [
            call({'order_1': {'some': 'here'}}),
            call({'order2': {}}),
        ]

    def test_it_should_jsonify_orders(self, protocol: Protocol, orders: IOrders | Mock):
        orders.jsonify_order = Mock(side_effect=[{'order_1': {'some': 'here'}}, {'order2': {}}])

        order_1 = object()
        order_2 = object()
        assert protocol.jsonify_order(order_1) == {'order_1': {'some': 'here'}}
        assert protocol.jsonify_order(order_2) == {'order2': {}}
        assert orders.jsonify_order.call_args_list == [
            call(order_1),
            call(order_2),
        ]

    def test_it_should_make_fields(self, protocol: Protocol, fields: IFields | Mock):
        field_1 = object()
        field_2 = object()

        fields.make_field = Mock(side_effect=[field_1, field_2])

        assert protocol.make_field({'field_1': {'some': 'here'}}) == field_1
        assert protocol.make_field({'field2': {}}) == field_2
        assert fields.make_field.call_args_list == [
            call({'field_1': {'some': 'here'}}),
            call({'field2': {}}),
        ]

    def test_it_should_jsonify_fields(self, protocol: Protocol, fields: IFields | Mock):
        fields.jsonify_field = Mock(side_effect=[{'field_1': {'some': 'here'}}, {'field2': {}}])

        field_1 = object()
        field_2 = object()
        assert protocol.jsonify_field(field_1) == {'field_1': {'some': 'here'}}
        assert protocol.jsonify_field(field_2) == {'field2': {}}
        assert fields.jsonify_field.call_args_list == [
            call(field_1),
            call(field_2),
        ]
