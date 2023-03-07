from pytest import fixture

from rmshared.content.taxonomy.core2 import fields
from rmshared.content.taxonomy.core2.protocols.fields import Fields


class TestFields:
    @fixture
    def fields_(self) -> Fields:
        return Fields()

    def test_it_should_make_field(self, fields_):
        assert fields_.make_field({'system-field': {}}) == fields.System(name='system-field')
        assert fields_.make_field({'custom-field': {'path': 'path.to.value'}}) == fields.Custom(name='custom-field', path='path.to.value')

    def test_it_should_jsonify_field(self, fields_):
        assert fields_.jsonify_field(fields.System(name='system-field')) == {'system-field': {}}
        assert fields_.jsonify_field(fields.Custom(name='custom-field', path='path.to.value')) == {'custom-field': {'path': 'path.to.value'}}
