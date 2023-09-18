from pytest import fixture

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core.protocols.db.fields import Fields


class TestFields:
    @fixture
    def protocol(self) -> Fields:
        return Fields()

    def test_system_fields(self, protocol: Fields):
        assert protocol.make_field(data=self.SYSTEM_FIELD_DATA) == self.SYSTEM_FIELD
        assert protocol.jsonify_field(field=self.SYSTEM_FIELD) == self.SYSTEM_FIELD_DATA

    SYSTEM_FIELD = fields.System(name='system-field')
    SYSTEM_FIELD_DATA = {'type': 'system', 'info': {'name': 'system-field'}}

    def test_custom_fields(self, protocol: Fields):
        assert protocol.make_field(data=self.CUSTOM_FIELD_DATA) == self.CUSTOM_FIELD
        assert protocol.jsonify_field(field=self.CUSTOM_FIELD) == self.CUSTOM_FIELD_DATA

    CUSTOM_FIELD = fields.Custom(name='custom-field', path='path.to.value')    
    CUSTOM_FIELD_DATA = {'type': 'custom', 'info': {'name': 'custom-field', 'path': 'path.to.value'}}
