from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core2 import ranges
from rmshared.content.taxonomy.core2.protocols.abc import IFields
from rmshared.content.taxonomy.core2.protocols.abc import IValues
from rmshared.content.taxonomy.core2.protocols.ranges import Ranges


class TestRanges:
    @fixture
    def ranges_(self, fields_: IFields, values_: IValues) -> Ranges:
        return Ranges(fields_, values_)

    @fixture
    def fields_(self) -> IFields | Mock:
        return Mock(spec=IFields)

    @fixture
    def values_(self) -> IValues | Mock:
        return Mock(spec=IValues)

    def test_it_should_make_range(self, ranges_, fields_: IFields, values_: IValues):
        fields_.make_field = Mock(side_effect=['field_1', 'field_2', 'field_3'])
        values_.make_value = Mock(side_effect=['value_1', 'value_2', 'value_3', 'value_4'])

        assert ranges_.make_range({'field': {'field_1': {}}, 'min': {'value_1': {}}, 'max': {'value_2': {}}}) == ranges.Between(
            field='field_1', min_value='value_1', max_value='value_2'
        )
        assert ranges_.make_range({'field': {'field_2': {}}, 'min': {'value_3': {}}}) == ranges.MoreThan(field='field_2', value='value_3')
        assert ranges_.make_range({'field': {'field_3': {}}, 'max': {'value_4': {}}}) == ranges.LessThan(field='field_3', value='value_4')
        assert fields_.make_field.call_args_list == [
            call({'field_1': {}}),
            call({'field_2': {}}),
            call({'field_3': {}}),
        ]
        assert values_.make_value.call_args_list == [
            call({'value_1': {}}),
            call({'value_2': {}}),
            call({'value_3': {}}),
            call({'value_4': {}}),
        ]

    def test_it_should_jsonify_range(self, ranges_, fields_: IFields, values_: IValues):
        fields_.jsonify_field = Mock(side_effect=[{'field_1': {}}, {'field_2': {}}, {'field_3': {}}])
        values_.jsonify_value = Mock(side_effect=[{'value_1': {}}, {'value_2': {}}, {'value_3': {}}, {'value_4': {}}])

        assert ranges_.jsonify_range(ranges.Between(field='field_1', min_value='value_1', max_value='value_2')) == {
            'field': {'field_1': {}},
            'min': {'value_1': {}},
            'max': {'value_2': {}},
        }
        assert ranges_.jsonify_range(ranges.MoreThan(field='field_2', value='value_3')) == {'field': {'field_2': {}}, 'min': {'value_3': {}}}
        assert ranges_.jsonify_range(ranges.LessThan(field='field_3', value='value_4')) == {'field': {'field_3': {}}, 'max': {'value_4': {}}}
        assert fields_.jsonify_field.call_args_list == [
            call('field_1'),
            call('field_2'),
            call('field_3'),
        ]
        assert values_.jsonify_value.call_args_list == [
            call('value_1'),
            call('value_2'),
            call('value_3'),
            call('value_4'),
        ]
