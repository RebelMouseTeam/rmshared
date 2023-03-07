from typing import Any
from typing import Callable
from typing import Mapping
from typing import Sequence
from typing import Type
from typing import TypeVar

from rmshared.tools import invert_dict
from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.core2 import filters
from rmshared.content.taxonomy.core2.protocols.abc import IFilters
from rmshared.content.taxonomy.core2.protocols.abc import ILabels
from rmshared.content.taxonomy.core2.protocols.abc import IRanges


class Filters(IFilters[filters.Filter]):
    F = TypeVar('F', bound=filters.Filter)

    def __init__(self, labels: ILabels, ranges: IRanges):
        self.labels = labels
        self.ranges = ranges
        self.filter_to_filter_name_map: Mapping[Type[filters.Filter], str] = {
            filters.AnyLabel: 'any_label',
            filters.NoLabels: 'no_labels',
            filters.AnyRange: 'any_range',
            filters.NoRanges: 'no_ranges',
        }
        self.filter_name_to_filter_map: Mapping[str, Type[filters.Filter]] = invert_dict(self.filter_to_filter_name_map)
        self.filter_to_factory_func_map: Mapping[Type[filters.Filter], Callable[[Any], filters.Filter]] = {
            filters.AnyLabel: self._make_any_label_filter,
            filters.NoLabels: self._make_no_labels_filter,
            filters.AnyRange: self._make_any_range_filter,
            filters.NoRanges: self._make_no_ranges_filter,
        }
        self.filter_to_jsonify_func_map: Mapping[Type[filters.Filter], Callable[[Filters.F], Sequence[Mapping[str, Any]]]] = {
            filters.AnyLabel: self._jsonify_labels_filter_info,
            filters.NoLabels: self._jsonify_labels_filter_info,
            filters.AnyRange: self._jsonify_ranges_filter_info,
            filters.NoRanges: self._jsonify_ranges_filter_info,
        }

    def make_filter(self, data):
        name, info = parse_name_and_info(data)
        filter_type = self.filter_name_to_filter_map[name]
        return self.filter_to_factory_func_map[filter_type](info)

    def jsonify_filter(self, filter_):
        name = self.filter_to_filter_name_map[type(filter_)]
        info = self.filter_to_jsonify_func_map[type(filter_)](filter_)
        return {name: info}

    def _make_any_label_filter(self, info: Any):
        return filters.AnyLabel(labels=tuple(map(self.labels.make_label, info)))

    def _make_no_labels_filter(self, info: Any):
        return filters.NoLabels(labels=tuple(map(self.labels.make_label, info)))

    def _jsonify_labels_filter_info(self, filter_: filters.AnyLabel | filters.NoLabels) -> Sequence[Mapping[str, Any]]:
        return list(map(self.labels.jsonify_label, filter_.labels))

    def _make_any_range_filter(self, info: Any):
        return filters.AnyRange(ranges=tuple(map(self.ranges.make_range, info)))

    def _make_no_ranges_filter(self, info: Any):
        return filters.NoRanges(ranges=tuple(map(self.ranges.make_range, info)))

    def _jsonify_ranges_filter_info(self, filter_: filters.AnyRange | filters.NoRanges) -> Sequence[Mapping[str, Any]]:
        return list(map(self.ranges.jsonify_range, filter_.ranges))
