from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core.encoders.abc import IFields
from rmshared.content.taxonomy.core.encoders.abc import IValues
from rmshared.content.taxonomy.core.encoders.keys.ranges import Ranges


class TestRanges:
    @fixture
    def encoder(self, fields_: IFields, values_: IValues) -> Ranges:
        return Ranges(fields=fields_, values=values_)

    @fixture
    def fields_(self) -> IFields | Mock:
        return Mock(spec=IFields)

    @fixture
    def values_(self) -> IValues | Mock:
        return Mock(spec=IValues)

    def test_between(self, encoder: Ranges, fields_: IFields, values_: IValues):
        fields_.encode_field = Mock(side_effect=['f_1'])
        values_.encode_value = Mock(side_effect=['v_1', 'v_2'])
        assert encoder.encode_range(ranges.Between(field='field_1', min_value='value_1', max_value='value_2')) == 'v_1<f_1<v_2'
        assert fields_.encode_field.call_args_list == [call('field_1')]
        assert values_.encode_value.call_args_list == [call('value_1'), call('value_2')]

    def test_less_than(self, encoder: Ranges, fields_: IFields, values_: IValues):
        fields_.encode_field = Mock(side_effect=['f_2'])
        values_.encode_value = Mock(side_effect=['v_3'])
        assert encoder.encode_range(ranges.LessThan(field='field_2', value='value_3')) == 'f_2<v_3'
        assert fields_.encode_field.call_args_list == [call('field_2')]
        assert values_.encode_value.call_args_list == [call('value_3')]

    def test_more_than(self, encoder: Ranges, fields_: IFields, values_: IValues):
        fields_.encode_field = Mock(side_effect=['f_3'])
        values_.encode_value = Mock(side_effect=['v_4'])
        assert encoder.encode_range(ranges.MoreThan(field='field_3', value='value_4')) == 'v_4<f_3'
        assert fields_.encode_field.call_args_list == [call('field_3')]
        assert values_.encode_value.call_args_list == [call('value_4')]
