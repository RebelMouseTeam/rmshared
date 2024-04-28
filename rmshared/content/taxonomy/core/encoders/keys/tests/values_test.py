from pytest import fixture

from rmshared.content.taxonomy.core.encoders.keys.values import Values


class TestValues:
    @fixture
    def encoder(self) -> Values:
        return Values()

    def test_values(self, encoder: Values):
        assert encoder.encode_value(value='some-value') == 'some-value'
        assert encoder.encode_value(value=1) == '1'
        assert encoder.encode_value(value=1.5) == '1.5'
        assert encoder.encode_value(value=[1, 2, 3]) == '[1, 2, 3]'
