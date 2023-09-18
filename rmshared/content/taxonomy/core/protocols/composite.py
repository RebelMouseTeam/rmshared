from rmshared.content.taxonomy.core.protocols.abc import IComposite
from rmshared.content.taxonomy.core.protocols.abc import IFilters
from rmshared.content.taxonomy.core.protocols.abc import IFields
from rmshared.content.taxonomy.core.protocols.abc import ILabels
from rmshared.content.taxonomy.core.protocols.abc import IRanges
from rmshared.content.taxonomy.core.protocols.abc import IValues
from rmshared.content.taxonomy.core.protocols.abc import IEvents


class Composite(IComposite):
    def __init__(self, filters: IFilters, labels: ILabels, ranges: IRanges, fields: IFields, events: IEvents, values: IValues):
        self.filters = filters
        self.labels = labels
        self.ranges = ranges
        self.fields = fields
        self.events = events
        self.values = values

    def jsonify_filter(self, filter_):
        return self.filters.jsonify_filter(filter_)

    def make_filter(self, data):
        return self.filters.make_filter(data)

    def make_label(self, data):
        return self.labels.make_label(data)

    def jsonify_label(self, label):
        return self.labels.jsonify_label(label)

    def make_range(self, data):
        return self.ranges.make_range(data)

    def jsonify_range(self, range_):
        return self.ranges.jsonify_range(range_)

    def make_field(self, data):
        return self.fields.make_field(data)

    def jsonify_field(self, field):
        return self.fields.jsonify_field(field)

    def make_event(self, data):
        return self.events.make_event(data)

    def jsonify_event(self, event):
        return self.events.jsonify_event(event)

    def make_value(self, data):
        return self.values.make_value(data)

    def jsonify_value(self, value):
        return self.values.jsonify_value(value)
