from rmshared.content.taxonomy import protocols
from rmshared.content.taxonomy.core2 import ranges


class Between(protocols.composites.IRanges.IProtocol[ranges.Between]):
    def __init__(self, fields: protocols.IFields, values: protocols.IValues):
        self.fields = fields
        self.values = values

    def get_keys(self):
        return {'field', 'min', 'max'}

    def make_range(self, data):
        return ranges.Between(
            field=self.fields.make_field(data['field']),
            min_value=self.values.make_value(data['min']),
            max_value=self.values.make_value(data['max']),
        )

    def jsonify_range(self, range_: ranges.Between):
        return {
            'field': self.fields.jsonify_field(range_.field),
            'min': self.values.jsonify_value(range_.min_value),
            'max': self.values.jsonify_value(range_.max_value),
        }


class LessThan(protocols.composites.IRanges.IProtocol[ranges.LessThan]):
    def __init__(self, fields: protocols.IFields, values: protocols.IValues):
        self.fields = fields
        self.values = values

    def get_keys(self):
        return {'field', 'max'}

    def make_range(self, data):
        return ranges.LessThan(
            field=self.fields.make_field(data['field']),
            value=self.values.make_value(data['max']),
        )

    def jsonify_range(self, range_: ranges.LessThan):
        return {
            'field': self.fields.jsonify_field(range_.field),
            'max': self.values.jsonify_value(range_.value),
        }


class MoreThan(protocols.composites.IRanges.IProtocol[ranges.MoreThan]):
    def __init__(self, fields: protocols.IFields, values: protocols.IValues):
        self.fields = fields
        self.values = values

    def get_keys(self):
        return {'field', 'min'}

    def make_range(self, data):
        return ranges.MoreThan(
            field=self.fields.make_field(data['field']),
            value=self.values.make_value(data['min']),
        )

    def jsonify_range(self, range_: ranges.MoreThan):
        return {
            'field': self.fields.jsonify_field(range_.field),
            'min': self.values.jsonify_value(range_.value),
        }
