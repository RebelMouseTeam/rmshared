from rmshared.content.taxonomy import protocols
from rmshared.content.taxonomy.core2 import fields


class System(protocols.composites.IFields.IProtocol[fields.System]):
    def get_keys(self):
        return set()

    def make_field(self, name, info):
        return fields.System(name=str(name))

    def jsonify_field(self, field: fields.System):
        return field.name, dict()


class Custom(protocols.composites.IFields.IProtocol[fields.Custom]):
    def get_keys(self):
        return {'path'}

    def make_field(self, name, info):
        return fields.Custom(name=str(name), path=str(info['path']))

    def jsonify_field(self, field: fields.Custom):
        return field.name, {'path': field.path}
