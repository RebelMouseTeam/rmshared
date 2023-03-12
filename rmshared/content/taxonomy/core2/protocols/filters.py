from rmshared.content.taxonomy import protocols
from rmshared.content.taxonomy.core2 import filters


class AnyLabel(protocols.composites.IFilters.IProtocol[filters.AnyLabel]):
    def __init__(self, labels: protocols.ILabels):
        self.labels = labels

    def get_keys(self):
        return {'any_label'}

    def make_filter(self, data) -> filters.AnyLabel:
        return filters.AnyLabel(labels=tuple(map(self.labels.make_label, data['any_label'])))

    def jsonify_filter(self, filter_: filters.AnyLabel):
        return {'any_label': list(map(self.labels.jsonify_label, filter_.labels))}


class NoLabels(protocols.composites.IFilters.IProtocol[filters.NoLabels]):
    def __init__(self, labels: protocols.ILabels):
        self.labels = labels

    def get_keys(self):
        return {'no_labels'}

    def make_filter(self, data) -> filters.NoLabels:
        return filters.NoLabels(labels=tuple(map(self.labels.make_label, data['no_labels'])))

    def jsonify_filter(self, filter_: filters.NoLabels):
        return {'no_labels': list(map(self.labels.jsonify_label, filter_.labels))}


class AnyRange(protocols.composites.IFilters.IProtocol[filters.AnyRange]):
    def __init__(self, ranges: protocols.IRanges):
        self.ranges = ranges

    def get_keys(self):
        return {'any_range'}

    def make_filter(self, data) -> filters.AnyRange:
        return filters.AnyRange(ranges=tuple(map(self.ranges.make_range, data['any_range'])))

    def jsonify_filter(self, filter_: filters.AnyRange):
        return {'any_range': list(map(self.ranges.jsonify_range, filter_.ranges))}


class NoRanges(protocols.composites.IFilters.IProtocol[filters.NoRanges]):
    def __init__(self, ranges: protocols.IRanges):
        self.ranges = ranges

    def get_keys(self):
        return {'no_ranges'}

    def make_filter(self, data) -> filters.NoRanges:
        return filters.NoRanges(ranges=tuple(map(self.ranges.make_range, data['no_ranges'])))

    def jsonify_filter(self, filter_: filters.NoRanges):
        return {'no_ranges': list(map(self.ranges.jsonify_range, filter_.ranges))}
