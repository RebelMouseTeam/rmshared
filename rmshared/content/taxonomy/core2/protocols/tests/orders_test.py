from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core2 import orders
from rmshared.content.taxonomy.core2.protocols.abc import IFields
from rmshared.content.taxonomy.core2.protocols.orders import Orders


class TestOrders:
    @fixture
    def orders_(self, fields_: IFields) -> Orders:
        return Orders(fields_)

    @fixture
    def fields_(self) -> IFields | Mock:
        return Mock(spec=IFields)

    def test_it_should_make_order(self, orders_, fields_: IFields):
        fields_.make_field = Mock(side_effect=['field_1', 'field_2'])

        assert orders_.make_order({'value': {'field': {'field_1': {}}, 'reverse': True}}) == orders.Value(field='field_1', reverse=True)
        assert orders_.make_order({'value': {'field': {'field_2': {}}, 'reverse': False}}) == orders.Value(field='field_2', reverse=False)
        assert fields_.make_field.call_args_list == [
            call({'field_1': {}}),
            call({'field_2': {}}),
        ]

    def test_it_should_jsonify_order(self, orders_, fields_: IFields):
        fields_.jsonify_field = Mock(side_effect=[{'field_1': {}}, {'field_2': {}}])

        assert orders_.jsonify_order(orders.Value(field='field_1', reverse=True)) == {'value': {'field': {'field_1': {}}, 'reverse': True}}
        assert orders_.jsonify_order(orders.Value(field='field_2', reverse=False)) == {'value': {'field': {'field_2': {}}, 'reverse': False}}
        assert fields_.jsonify_field.call_args_list == [
            call('field_1'),
            call('field_2'),
        ]
