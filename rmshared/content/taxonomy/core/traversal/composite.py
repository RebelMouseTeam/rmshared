from rmshared.content.taxonomy.core.traversal.abc import IComposite
from rmshared.content.taxonomy.core.traversal.abc import IFilters
from rmshared.content.taxonomy.core.traversal.abc import ILabels
from rmshared.content.taxonomy.core.traversal.abc import IRanges
from rmshared.content.taxonomy.core.traversal.abc import IEvents


class Composite(IComposite):
    def __init__(self, filters: IFilters, labels: ILabels, ranges: IRanges, events: IEvents):
        self.filters = filters
        self.labels = labels
        self.ranges = ranges
        self.events = events

    def traverse_filters(self, filters_, visitor):
        self.filters.traverse_filters(filters_, visitor)

    def traverse_labels(self, labels_, visitor):
        self.labels.traverse_labels(labels_, visitor)

    def traverse_ranges(self, ranges_, visitor):
        self.ranges.traverse_ranges(ranges_, visitor)

    def traverse_events(self, events_, visitor):
        self.events.traverse_events(events_, visitor)
