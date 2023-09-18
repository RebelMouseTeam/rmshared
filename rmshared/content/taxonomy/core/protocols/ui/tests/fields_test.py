from pytest import fixture

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core.protocols.ui.fields import Fields


class TestFields:
    @fixture
    def protocol(self) -> Fields:
        return Fields()

    def test_system_fields(self, protocol: Fields):
        assert protocol.make_field(data={'system-field': {}}) == fields.System(name='system-field')
        assert protocol.jsonify_field(field=fields.System(name='system-field')) == {'system-field': {}}

    def test_custom_fields(self, protocol: Fields):
        assert protocol.make_field(data={'custom-field': {'path': 'path.to.value'}}) == fields.Custom(name='custom-field', path='path.to.value')
        assert protocol.jsonify_field(field=fields.Custom(name='custom-field', path='path.to.value')) == {'custom-field': {'path': 'path.to.value'}}
