from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core.protocols.abc import IFields
from rmshared.content.taxonomy.core.protocols.abc import IValues
from rmshared.content.taxonomy.core.protocols.ui.ranges import Ranges


class TestRanges:
    @fixture
    def protocol(self, fields_: IFields, values_: IValues) -> Ranges:
        return Ranges(fields=fields_, values=values_)

    @fixture
    def fields_(self) -> IFields | Mock:
        return Mock(spec=IFields)

    @fixture
    def values_(self) -> IValues | Mock:
        return Mock(spec=IValues)

    def test_between(self, protocol: Ranges, fields_: IFields, values_: IValues):
        fields_.make_field = Mock(side_effect=['field_1'])
        values_.make_value = Mock(side_effect=['value_1', 'value_2'])
        fields_.jsonify_field = Mock(side_effect=[{'field_1': {}}])
        values_.jsonify_value = Mock(side_effect=[{'value_1': {}}, {'value_2': {}}])

        assert protocol.make_range({'field': {'field_1': {}}, 'min': {'value_1': {}}, 'max': {'value_2': {}}}) == ranges.Between(
            field='field_1', min_value='value_1', max_value='value_2',
        )
        assert protocol.jsonify_range(ranges.Between(field='field_1', min_value='value_1', max_value='value_2')) == {
            'field': {'field_1': {}}, 'min': {'value_1': {}}, 'max': {'value_2': {}},
        }
        assert fields_.make_field.call_args_list == [call({'field_1': {}})]
        assert values_.make_value.call_args_list == [call({'value_1': {}}), call({'value_2': {}})]
        assert fields_.jsonify_field.call_args_list == [call('field_1')]
        assert values_.jsonify_value.call_args_list == [call('value_1'), call('value_2')]

    def test_less_than(self, protocol: Ranges, fields_: IFields, values_: IValues):
        fields_.make_field = Mock(side_effect=['field_2'])
        values_.make_value = Mock(side_effect=['value_3'])
        fields_.jsonify_field = Mock(side_effect=[{'field_2': {}}])
        values_.jsonify_value = Mock(side_effect=[{'value_3': {}}])

        assert protocol.make_range({'field': {'field_2': {}}, 'max': {'value_3': {}}}) == ranges.LessThan(field='field_2', value='value_3')
        assert protocol.jsonify_range(ranges.LessThan(field='field_2', value='value_3')) == {'field': {'field_2': {}}, 'max': {'value_3': {}}}
        assert fields_.make_field.call_args_list == [call({'field_2': {}})]
        assert values_.make_value.call_args_list == [call({'value_3': {}})]
        assert fields_.jsonify_field.call_args_list == [call('field_2')]
        assert values_.jsonify_value.call_args_list == [call('value_3')]

    def test_more_than(self, protocol: Ranges, fields_: IFields, values_: IValues):
        fields_.make_field = Mock(side_effect=['field_3'])
        values_.make_value = Mock(side_effect=['value_4'])
        fields_.jsonify_field = Mock(side_effect=[{'field_3': {}}])
        values_.jsonify_value = Mock(side_effect=[{'value_4': {}}])

        assert protocol.make_range({'field': {'field_3': {}}, 'min': {'value_4': {}}}) == ranges.MoreThan(field='field_3', value='value_4')
        assert protocol.jsonify_range(ranges.MoreThan(field='field_3', value='value_4')) == {'field': {'field_3': {}}, 'min': {'value_4': {}}}
        assert fields_.make_field.call_args_list == [call({'field_3': {}})]
        assert values_.make_value.call_args_list == [call({'value_4': {}})]
        assert fields_.jsonify_field.call_args_list == [call('field_3')]
        assert values_.jsonify_value.call_args_list == [call('value_4')]
