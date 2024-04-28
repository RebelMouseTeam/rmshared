from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core.encoders.abc import IFields
from rmshared.content.taxonomy.core.encoders.abc import IValues
from rmshared.content.taxonomy.core.encoders.keys.labels import Labels


class TestLabels:
    @fixture
    def encoder(self, fields_: IFields, values_: IValues) -> Labels:
        return Labels(fields=fields_, values=values_)

    @fixture
    def fields_(self) -> IFields | Mock:
        return Mock(spec=IFields)

    @fixture
    def values_(self) -> IValues | Mock:
        return Mock(spec=IValues)

    def test_value(self, encoder: Labels, fields_: IFields, values_: IValues):
        fields_.encode_field = Mock(side_effect=['f_1'])
        values_.encode_value = Mock(side_effect=['v_1'])
        assert encoder.encode_label(labels.Value(field='field_1', value='value_1')) == 'f_1=v_1'
        assert values_.encode_value.call_args_list == [call('value_1')]
        assert fields_.encode_field.call_args_list == [call('field_1')]

    def test_badge(self, encoder: Labels, fields_: IFields):
        fields_.encode_field = Mock(side_effect=['f_2'])
        assert encoder.encode_label(labels.Badge(field='field_2')) == 'f_2+'
        assert fields_.encode_field.call_args_list == [call('field_2')]

    def test_empty(self, encoder: Labels, fields_: IFields):
        fields_.encode_field = Mock(side_effect=['f_3'])
        assert encoder.encode_label(labels.Empty(field='field_3')) == 'f_3-'
        assert fields_.encode_field.call_args_list == [call('field_3')]
