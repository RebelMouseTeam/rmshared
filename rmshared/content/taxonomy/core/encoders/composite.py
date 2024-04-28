from rmshared.content.taxonomy.core.encoders.abc import IComposite
from rmshared.content.taxonomy.core.encoders.abc import IFilters
from rmshared.content.taxonomy.core.encoders.abc import ILabels
from rmshared.content.taxonomy.core.encoders.abc import IRanges
from rmshared.content.taxonomy.core.encoders.abc import IFields
from rmshared.content.taxonomy.core.encoders.abc import IEvents
from rmshared.content.taxonomy.core.encoders.abc import IValues


class Composite(IComposite):
    def __init__(self, filters: IFilters, labels: ILabels, ranges: IRanges, fields: IFields, events: IEvents, values: IValues):
        self.filters = filters
        self.labels = labels
        self.ranges = ranges
        self.fields = fields
        self.events = events
        self.values = values

    def encode_filter(self, filter_):
        return self.filters.encode_filter(filter_)

    def encode_label(self, label):
        return self.labels.encode_label(label)

    def encode_range(self, range_):
        return self.ranges.encode_range(range_)

    def encode_field(self, field):
        return self.fields.encode_field(field)

    def encode_event(self, event):
        return self.events.encode_event(event)

    def encode_value(self, value):
        return self.values.encode_value(value)
