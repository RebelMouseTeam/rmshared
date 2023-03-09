from rmshared.content.taxonomy import protocols
from rmshared.content.taxonomy.core2 import filters


class AnyLabel(protocols.builders.IFilters.IProtocol[filters.AnyLabel]):
    def __init__(self, labels: protocols.ILabels):
        self.labels = labels

    @classmethod
    def get_name(cls):
        return 'any_label'

    def make_filter(self, info):
        return filters.AnyLabel(labels=tuple(map(self.labels.make_label, info)))

    def jsonify_filter_info(self, filter_: filters.AnyLabel):
        return list(map(self.labels.jsonify_label, filter_.labels))


class NoLabels(protocols.builders.IFilters.IProtocol[filters.NoLabels]):
    def __init__(self, labels: protocols.ILabels):
        self.labels = labels

    @classmethod
    def get_name(cls):
        return 'no_labels'

    def make_filter(self, info):
        return filters.NoLabels(labels=tuple(map(self.labels.make_label, info)))

    def jsonify_filter_info(self, filter_: filters.NoLabels):
        return list(map(self.labels.jsonify_label, filter_.labels))


class AnyRange(protocols.builders.IFilters.IProtocol[filters.AnyRange]):
    def __init__(self, ranges: protocols.IRanges):
        self.ranges = ranges

    @classmethod
    def get_name(cls):
        return 'any_range'

    def make_filter(self, info):
        return filters.AnyRange(ranges=tuple(map(self.ranges.make_range, info)))

    def jsonify_filter_info(self, filter_: filters.AnyRange):
        return list(map(self.ranges.jsonify_range, filter_.ranges))


class NoRanges(protocols.builders.IFilters.IProtocol[filters.NoRanges]):
    def __init__(self, ranges: protocols.IRanges):
        self.ranges = ranges

    @classmethod
    def get_name(cls):
        return 'no_ranges'

    def make_filter(self, info):
        return filters.NoRanges(ranges=tuple(map(self.ranges.make_range, info)))

    def jsonify_filter_info(self, filter_: filters.NoRanges):
        return list(map(self.ranges.jsonify_range, filter_.ranges))
