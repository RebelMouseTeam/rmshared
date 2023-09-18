from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core.protocols.abc import IFields
from rmshared.content.taxonomy.core.protocols.abc import IValues
from rmshared.content.taxonomy.core.protocols.ui.labels import Labels


class TestLabels:
    @fixture
    def protocol(self, fields_: IFields, values_: IValues) -> Labels:
        return Labels(fields=fields_, values=values_)

    @fixture
    def fields_(self) -> IFields | Mock:
        return Mock(spec=IFields)

    @fixture
    def values_(self) -> IValues | Mock:
        return Mock(spec=IValues)

    def test_value(self, protocol: Labels, fields_: IFields, values_: IValues):
        fields_.make_field = Mock(side_effect=['field_1'])
        values_.make_value = Mock(side_effect=['value_1'])
        fields_.jsonify_field = Mock(side_effect=[{'field_1': {}}])
        values_.jsonify_value = Mock(side_effect=[{'value_1': {}}])

        assert protocol.make_label({'value': {'field': {'field_1': {}}, 'value': {'value_1': {}}}}) == labels.Value(field='field_1', value='value_1')
        assert protocol.jsonify_label(labels.Value(field='field_1', value='value_1')) == {'value': {'field': {'field_1': {}}, 'value': {'value_1': {}}}}
        assert values_.make_value.call_args_list == [call({'value_1': {}})]
        assert fields_.make_field.call_args_list == [call({'field_1': {}})]
        assert values_.jsonify_value.call_args_list == [call('value_1')]
        assert fields_.jsonify_field.call_args_list == [call('field_1')]

    def test_badge(self, protocol: Labels, fields_: IFields):
        fields_.make_field = Mock(side_effect=['field_2'])
        fields_.jsonify_field = Mock(side_effect=[{'field_2': {}}])

        assert protocol.make_label({'badge': {'field': {'field_2': {}}}}) == labels.Badge(field='field_2')
        assert protocol.jsonify_label(labels.Badge(field='field_2')) == {'badge': {'field': {'field_2': {}}}}
        assert fields_.make_field.call_args_list == [call({'field_2': {}})]
        assert fields_.jsonify_field.call_args_list == [call('field_2')]

    def test_empty(self, protocol: Labels, fields_: IFields):
        fields_.make_field = Mock(side_effect=['field_3'])
        fields_.jsonify_field = Mock(side_effect=[{'field_3': {}}])

        assert protocol.make_label({'empty': {'field': {'field_3': {}}}}) == labels.Empty(field='field_3')
        assert protocol.jsonify_label(labels.Empty(field='field_3')) == {'empty': {'field': {'field_3': {}}}}
        assert fields_.make_field.call_args_list == [call({'field_3': {}})]
        assert fields_.jsonify_field.call_args_list == [call('field_3')]
