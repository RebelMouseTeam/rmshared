from pytest import fixture

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core.encoders.keys.fields import Fields


class TestFields:
    @fixture
    def encoder(self) -> Fields:
        return Fields()

    def test_system_fields(self, encoder: Fields):
        assert encoder.encode_field(field=fields.System(name='some-field')) == 'some-field'

    def test_custom_fields(self, encoder: Fields):
        assert encoder.encode_field(field=fields.Custom(name='some-field', path='path.to.value')) == 'some-field:path.to.value'
