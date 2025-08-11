from rmshared.content.taxonomy.core.sql.compiling.abc import IComposite
from rmshared.content.taxonomy.core.sql.compiling.abc import IFilters
from rmshared.content.taxonomy.core.sql.compiling.abc import ILabels
from rmshared.content.taxonomy.core.sql.compiling.abc import IRanges
from rmshared.content.taxonomy.core.sql.compiling.abc import IFields
from rmshared.content.taxonomy.core.sql.compiling.abc import IEvents
from rmshared.content.taxonomy.core.sql.compiling.abc import IValues


class Composite(IComposite):
    def __init__(self, filters: IFilters, labels: ILabels, ranges: IRanges, fields: IFields, events: IEvents, values: IValues):
        self.filters = filters
        self.labels = labels
        self.ranges = ranges
        self.fields = fields
        self.events = events
        self.values = values

    def make_tree_from_filter(self, filter_):
        return self.filters.make_tree_from_filter(filter_)

    def make_tree_from_labels(self, labels_, matcher):
        return self.labels.make_tree_from_labels(labels_, matcher)

    def make_tree_from_ranges(self, ranges_, matcher):
        return self.ranges.make_tree_from_ranges(ranges_, matcher)

    def make_tree_from_field(self, field):
        return self.fields.make_tree_from_field(field)

    def make_field_operations(self, field):  # TODO: Doesn't fit the pattern --> probably there's a better way (@see the matchers above)
        return self.fields.make_field_operations(field)

    def make_tree_from_event(self, event):
        return self.events.make_tree_from_event(event)

    def make_tree_from_value(self, value):
        return self.values.make_tree_from_value(value)
