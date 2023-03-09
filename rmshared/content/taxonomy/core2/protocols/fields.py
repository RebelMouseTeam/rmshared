from rmshared.content.taxonomy import protocols
from rmshared.content.taxonomy.core2 import fields


class System(protocols.builders.IFields.IProtocol[fields.System]):
    @classmethod
    def get_keys(cls):
        return set()

    def make_field(self, name, info):
        return fields.System(name=str(name))

    def jsonify_field(self, field_: fields.System):
        return field_.name, dict()


class Custom(protocols.builders.IFields.IProtocol[fields.Custom]):
    @classmethod
    def get_keys(cls):
        return {'path'}

    def make_field(self, name, info):
        return fields.Custom(name=str(name), path=str(info['path']))

    def jsonify_field(self, field_: fields.Custom):
        return field_.name, {'path': field_.path}
