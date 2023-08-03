from rmshared.content.taxonomy.visitors.abc import IFilters
from rmshared.content.taxonomy.visitors.abc import ILabels
from rmshared.content.taxonomy.visitors.abc import IRanges
from rmshared.content.taxonomy.visitors.abc import IFields
from rmshared.content.taxonomy.visitors.abc import IValues
from rmshared.content.taxonomy.visitors.abc import IVisitor


class Visitor(IVisitor):
    def __init__(self, filters: IFilters, labels: ILabels, ranges: IRanges, fields: IFields, values: IValues):
        self.filters = filters
        self.labels = labels
        self.ranges = ranges
        self.fields = fields
        self.values = values

    def visit_filters(self, filters):
        return map(self.filters.visit_filter, filters)

    def visit_label(self, label):
        return self.labels.visit_label(label)

    def visit_range(self, range_):
        return self.ranges.visit_range(range_)

    def visit_field(self, field):
        return self.fields.visit_field(field)

    def visit_value(self, value):
        return self.values.visit_value(value)
