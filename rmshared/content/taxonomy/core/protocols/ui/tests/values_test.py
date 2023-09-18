from pytest import fixture

from rmshared.content.taxonomy.core.protocols.ui.values import Values


class TestValues:
    @fixture
    def protocol(self) -> Values:
        return Values()

    def test_values(self, protocol: Values):
        assert protocol.make_value(data='some-value') == 'some-value'
        assert protocol.make_value(data=1) == 1
        assert protocol.make_value(data=1.5) == 1.5
        assert protocol.jsonify_value(value='some-value') == 'some-value'
        assert protocol.jsonify_value(value=1) == 1
        assert protocol.jsonify_value(value=1.5) == 1.5
