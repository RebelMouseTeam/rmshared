from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core2 import orders
from rmshared.content.taxonomy.core2 import protocols
from rmshared.content.taxonomy.protocols import IFields


class TestOrders:
    @fixture
    def fields_(self) -> IFields | Mock:
        return Mock(spec=IFields)

    def test_value(self, fields_: IFields):
        fields_.make_field = Mock(side_effect=['field_1', 'field_2'])
        fields_.jsonify_field = Mock(side_effect=[{'field_1': {}}, {'field_2': {}}])

        protocol = protocols.orders.Value(fields_)

        assert protocol.get_name() == 'value'
        assert protocol.make_order({'field': {'field_1': {}}, 'reverse': True}) == orders.Value(field='field_1', reverse=True)
        assert protocol.make_order({'field': {'field_2': {}}, 'reverse': False}) == orders.Value(field='field_2', reverse=False)
        assert protocol.jsonify_order_info(orders.Value(field='field_1', reverse=True)) == {'field': {'field_1': {}}, 'reverse': True}
        assert protocol.jsonify_order_info(orders.Value(field='field_2', reverse=False)) == {'field': {'field_2': {}}, 'reverse': False}
        assert fields_.make_field.call_args_list == [call({'field_1': {}}), call({'field_2': {}})]
        assert fields_.jsonify_field.call_args_list == [call('field_1'), call('field_2')]
