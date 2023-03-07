from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core2 import labels
from rmshared.content.taxonomy.core2.protocols.abc import IFields
from rmshared.content.taxonomy.core2.protocols.abc import IValues
from rmshared.content.taxonomy.core2.protocols.labels import Labels


class TestLabels:
    @fixture
    def labels_(self, fields_: IFields, values_: IValues) -> Labels:
        return Labels(fields_, values_)

    @fixture
    def fields_(self) -> IFields | Mock:
        return Mock(spec=IFields)

    @fixture
    def values_(self) -> IValues | Mock:
        return Mock(spec=IValues)

    def test_it_should_make_label(self, labels_, fields_: IFields, values_: IValues):
        fields_.make_field = Mock(side_effect=['field_1', 'field_2', 'field_3'])
        values_.make_value = Mock(side_effect=['value_1'])

        assert labels_.make_label({'value': {'field': {'field_1': {}}, 'value': {'value_1': {}}}}) == labels.Value(field='field_1', value='value_1')
        assert labels_.make_label({'badge': {'field': {'field_2': {}}}}) == labels.Badge(field='field_2')
        assert labels_.make_label({'empty': {'field': {'field_3': {}}}}) == labels.Empty(field='field_3')
        assert fields_.make_field.call_args_list == [
            call({'field_1': {}}),
            call({'field_2': {}}),
            call({'field_3': {}}),
        ]
        assert values_.make_value.call_args_list == [
            call({'value_1': {}}),
        ]

    def test_it_should_jsonify_label(self, labels_, fields_: IFields, values_: IValues):
        fields_.jsonify_field = Mock(side_effect=[{'field_1': {}}, {'field_2': {}}, {'field_3': {}}])
        values_.jsonify_value = Mock(side_effect=[{'value_1': {}}])

        assert labels_.jsonify_label(labels.Value(field='field_1', value='value_1')) == {'value': {'field': {'field_1': {}}, 'value': {'value_1': {}}}}
        assert labels_.jsonify_label(labels.Badge(field='field_2')) == {'badge': {'field': {'field_2': {}}}}
        assert labels_.jsonify_label(labels.Empty(field='field_3')) == {'empty': {'field': {'field_3': {}}}}
        assert fields_.jsonify_field.call_args_list == [
            call('field_1'),
            call('field_2'),
            call('field_3'),
        ]
        assert values_.jsonify_value.call_args_list == [
            call('value_1'),
        ]
