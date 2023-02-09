from itertools import chain
from typing import Callable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.typings import read_only

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import filters
from rmshared.content.taxonomy.abc import Filter
from rmshared.content.taxonomy.mappers.abc import IFilters
from rmshared.content.taxonomy.mappers.abc import ILabels
from rmshared.content.taxonomy.mappers.abc import IRanges


class Filters(IFilters):
    AnyFilter = TypeVar('AnyFilter', bound=Filter)

    def __init__(self, labels: ILabels, ranges: IRanges):
        self.labels = labels
        self.ranges = ranges
        self.filter_to_factory_func_map: Mapping[Type['Filters.AnyFilter'], Callable[['Filters.AnyFilter'], core.Filter]] = {
            filters.AnyLabel: self._map_any_label_filter,
            filters.NoLabels: self._map_no_labels_filter,
            filters.AnyRange: self._map_any_range_filter,
            filters.NoRanges: self._map_no_ranges_filter,
            filters.Phrase: self._map_phrase_filter,
        }

    def map_filters(self, filters_):
        return map(self._map_filter, filters_)

    def _map_filter(self, filter_: Filter) -> core.Filter:
        return self.filter_to_factory_func_map[type(filter_)](filter_)

    def _map_any_label_filter(self, filter_: filters.AnyLabel) -> core.filters.AnyLabel:
        return core.filters.AnyLabel(labels=tuple(map(self.labels.map_label, filter_.labels)))

    def _map_no_labels_filter(self, filter_: filters.NoLabels) -> core.filters.NoLabels:
        return core.filters.NoLabels(labels=tuple(map(self.labels.map_label, filter_.labels)))

    def _map_any_range_filter(self, filter_: filters.AnyRange) -> core.filters.AnyRange:
        return core.filters.AnyRange(ranges=tuple(chain.from_iterable(map(self.ranges.map_range, filter_.ranges))))

    def _map_no_ranges_filter(self, filter_: filters.NoRanges) -> core.filters.NoRanges:
        return core.filters.NoRanges(ranges=tuple(chain.from_iterable(map(self.ranges.map_range, filter_.ranges))))

    @staticmethod
    def _map_phrase_filter(filter_: filters.Phrase) -> core.filters.Phrase:
        return core.filters.Phrase(
            phrase=filter_.phrase,
            payload=read_only({
                'syntax': filter_.syntax,
                'weights': filter_.weights,
            }),
        )
