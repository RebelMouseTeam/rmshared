from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.protocols.abc import IFilters
from rmshared.content.taxonomy.protocols.abc import IOrders
from rmshared.content.taxonomy.protocols.protocol import Protocol


class TestProtocol:
    @fixture
    def protocol(self, filters: IFilters, orders: IOrders) -> Protocol:
        return Protocol(filters, orders)

    @fixture
    def filters(self) -> IFilters | Mock:
        return Mock(spec=IFilters)

    @fixture
    def orders(self) -> IOrders | Mock:
        return Mock(spec=IOrders)

    def test_it_should_make_filters(self, protocol: Protocol, filters: IFilters | Mock, orders: IOrders | Mock):
        filter_1 = object()
        filter_2 = object()

        filters.make_filter = Mock(side_effect=[filter_1, filter_2])

        data = [{'filter_1': {'some': 'here'}}, {'filter2': {}}]
        assert list(protocol.make_filters(data)) == [filter_1, filter_2]
        assert filters.make_filter.call_args_list == [
            call({'filter_1': {'some': 'here'}}),
            call({'filter2': {}}),
        ]

    def test_it_should_jsonify_filters(self, protocol: Protocol, filters: IFilters | Mock, orders: IOrders | Mock):
        filters.jsonify_filter = Mock(side_effect=[{'filter_1': {'some': 'here'}}, {'filter2': {}}])

        filter_1 = object()
        filter_2 = object()
        assert protocol.jsonify_filters([filter_1, filter_2]) == [{'filter_1': {'some': 'here'}}, {'filter2': {}}]
        assert filters.jsonify_filter.call_args_list == [
            call(filter_1),
            call(filter_2),
        ]

    def test_it_should_make_orders(self, protocol: Protocol, filters: IFilters | Mock, orders: IOrders | Mock):
        order_1 = object()
        order_2 = object()

        orders.make_order = Mock(side_effect=[order_1, order_2])

        assert protocol.make_order({'order_1': {'some': 'here'}}) == order_1
        assert protocol.make_order({'order2': {}}) == order_2
        assert orders.make_order.call_args_list == [
            call({'order_1': {'some': 'here'}}),
            call({'order2': {}}),
        ]

    def test_it_should_jsonify_orders(self, protocol: Protocol, filters: IFilters | Mock, orders: IOrders | Mock):
        orders.jsonify_order = Mock(side_effect=[{'order_1': {'some': 'here'}}, {'order2': {}}])

        order_1 = object()
        order_2 = object()
        assert protocol.jsonify_order(order_1) == {'order_1': {'some': 'here'}}
        assert protocol.jsonify_order(order_2) == {'order2': {}}
        assert orders.jsonify_order.call_args_list == [
            call(order_1),
            call(order_2),
        ]
