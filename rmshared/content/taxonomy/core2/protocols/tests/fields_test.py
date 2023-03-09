from rmshared.content.taxonomy.core2 import fields
from rmshared.content.taxonomy.core2 import protocols


class TestFields:
    def test_system_fields(self):
        protocol = protocols.fields.System()
        assert protocol.get_keys() == set()
        assert protocol.make_field(name='system-field', info={}) == fields.System(name='system-field')
        assert protocol.jsonify_field(fields.System(name='system-field')) == ('system-field', {})

    def test_custom_fields(self):
        protocol = protocols.fields.Custom()
        assert protocol.get_keys() == {'path'}
        assert protocol.make_field('custom-field', {'path': 'path.to.value'}) == fields.Custom(name='custom-field', path='path.to.value')
        assert protocol.jsonify_field(fields.Custom(name='custom-field', path='path.to.value')) == ('custom-field', {'path': 'path.to.value'})
