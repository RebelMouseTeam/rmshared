from pytest import fixture

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core.data import Fields


class TestFields:
    @fixture
    def data(self) -> Fields:
        return Fields()

    def test_it_should_make_fields(self, data: Fields):
        assert data.make_field({'type': 'system', 'info': {'name': 'foo'}}) == fields.System(name='foo')
        assert data.make_field({'type': 'custom', 'info': {'name': 'foo', 'path': 'bar'}}) == fields.Custom(name='foo', path='bar')

    def test_it_should_make_fields_data(self, data: Fields):
        assert data.make_field_data(fields.System(name='foo')) == {'type': 'system', 'info': {'name': 'foo'}}
        assert data.make_field_data(fields.Custom(name='foo', path='bar')) == {'type': 'custom', 'info': {'name': 'foo', 'path': 'bar'}}
