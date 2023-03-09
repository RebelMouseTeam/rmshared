from rmshared.content.taxonomy import protocols
from rmshared.content.taxonomy.core2 import labels


class Value(protocols.builders.ILabels.IProtocol[labels.Value]):
    def __init__(self, fields: protocols.IFields, values: protocols.IValues):
        self.fields = fields
        self.values = values

    @classmethod
    def get_name(cls):
        return 'value'

    def make_label(self, info):
        return labels.Value(
            field=self.fields.make_field(info['field']),
            value=self.values.make_value(info['value']),
        )

    def jsonify_label_info(self, label_: labels.Value):
        return {
            'field': self.fields.jsonify_field(label_.field),
            'value': self.values.jsonify_value(label_.value),
        }


class Badge(protocols.builders.ILabels.IProtocol[labels.Badge]):
    def __init__(self, fields: protocols.IFields):
        self.fields = fields

    @classmethod
    def get_name(cls):
        return 'badge'

    def make_label(self, info):
        return labels.Badge(
            field=self.fields.make_field(info['field']),
        )

    def jsonify_label_info(self, label_: labels.Badge):
        return {
            'field': self.fields.jsonify_field(label_.field),
        }


class Empty(protocols.builders.ILabels.IProtocol[labels.Empty]):
    def __init__(self, fields: protocols.IFields):
        self.fields = fields

    @classmethod
    def get_name(cls):
        return 'empty'

    def make_label(self, info):
        return labels.Empty(
            field=self.fields.make_field(info['field']),
        )

    def jsonify_label_info(self, label_: labels.Empty):
        return {
            'field': self.fields.jsonify_field(label_.field),
        }
