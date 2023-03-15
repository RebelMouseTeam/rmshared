from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core import orders
from rmshared.content.taxonomy.core import protocols
from rmshared.content.taxonomy.protocols import IFields


class TestOrders:
    @fixture
    def fields(self) -> IFields | Mock:
        return Mock(spec=IFields)

    def test_value(self, fields: IFields):
        fields.make_field = Mock(side_effect=['field_1', 'field_2'])
        fields.jsonify_field = Mock(side_effect=[{'field_1': {}}, {'field_2': {}}])

        protocol = protocols.orders.Value(fields)

        assert protocol.get_keys() == {'value'}
        assert protocol.make_order({'value': {'field': {'field_1': {}}, 'reverse': True}}) == orders.Value(field='field_1', reverse=True)
        assert protocol.make_order({'value': {'field': {'field_2': {}}, 'reverse': False}}) == orders.Value(field='field_2', reverse=False)
        assert protocol.jsonify_order(orders.Value(field='field_1', reverse=True)) == {'value': {'field': {'field_1': {}}, 'reverse': True}}
        assert protocol.jsonify_order(orders.Value(field='field_2', reverse=False)) == {'value': {'field': {'field_2': {}}, 'reverse': False}}
        assert fields.make_field.call_args_list == [call({'field_1': {}}), call({'field_2': {}})]
        assert fields.jsonify_field.call_args_list == [call('field_1'), call('field_2')]
