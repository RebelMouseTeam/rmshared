from rmshared.content.taxonomy import protocols
from rmshared.content.taxonomy.core2 import labels


class Value(protocols.composites.ILabels.IProtocol[labels.Value]):
    def __init__(self, fields: protocols.IFields, values: protocols.IValues):
        self.fields = fields
        self.values = values

    def get_keys(self):
        return {'value'}

    def make_label(self, data):
        return labels.Value(
            field=self.fields.make_field(data['value']['field']),
            value=self.values.make_value(data['value']['value']),
        )

    def jsonify_label(self, label: labels.Value):
        return {'value': {
            'field': self.fields.jsonify_field(label.field),
            'value': self.values.jsonify_value(label.value),
        }}


class Badge(protocols.composites.ILabels.IProtocol[labels.Badge]):
    def __init__(self, fields: protocols.IFields):
        self.fields = fields

    def get_keys(self):
        return {'badge'}

    def make_label(self, data):
        return labels.Badge(
            field=self.fields.make_field(data['badge']['field']),
        )

    def jsonify_label(self, label: labels.Badge):
        return {'badge': {
            'field': self.fields.jsonify_field(label.field),
        }}


class Empty(protocols.composites.ILabels.IProtocol[labels.Empty]):
    def __init__(self, fields: protocols.IFields):
        self.fields = fields

    def get_keys(self):
        return {'empty'}

    def make_label(self, data):
        return labels.Empty(
            field=self.fields.make_field(data['empty']['field']),
        )

    def jsonify_label(self, label: labels.Empty):
        return {'empty': {
            'field': self.fields.jsonify_field(label.field),
        }}
