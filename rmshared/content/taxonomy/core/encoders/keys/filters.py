from typing import Callable
from typing import Iterable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core.encoders.abc import LabelIn
from rmshared.content.taxonomy.core.encoders.abc import RangeIn
from rmshared.content.taxonomy.core.encoders.abc import IFilters
from rmshared.content.taxonomy.core.encoders.abc import ILabels
from rmshared.content.taxonomy.core.encoders.abc import IRanges

Filter = TypeVar('Filter', bound=filters.Filter)


class Filters(IFilters[filters.Filter, str]):
    def __init__(self, labels: ILabels, ranges: IRanges):
        self.labels = labels
        self.ranges = ranges
        self.filter_to_delegate_map: Mapping[Type[Filter], Callable[[Filter], str]] = ensure_map_is_complete(filters.Filter, {
            filters.AnyLabel: self._encode_any_label,
            filters.NoLabels: self._encode_no_labels,
            filters.AnyRange: self._encode_any_range,
            filters.NoRanges: self._encode_no_ranges,
        })

    def encode_filter(self, filter_):
        return ''.join(self.filter_to_delegate_map[type(filter_)](filter_))

    def _encode_any_label(self, filter_: filters.AnyLabel):
        labels = self._encode_labels(filter_.labels)
        return f'+l({labels})'

    def _encode_no_labels(self, filter_: filters.NoLabels):
        labels = self._encode_labels(filter_.labels)
        return f'-l({labels})'

    def _encode_labels(self, labels_: Iterable[LabelIn]) -> str:
        return ','.join(sorted(map(self.labels.encode_label, labels_)))

    def _encode_any_range(self, filter_: filters.AnyRange):
        ranges = self._encode_ranges(filter_.ranges)
        return f'+r({ranges})'

    def _encode_no_ranges(self, filter_: filters.NoRanges):
        ranges = self._encode_ranges(filter_.ranges)
        return f'-r({ranges})'

    def _encode_ranges(self, ranges_: Iterable[RangeIn]) -> str:
        return ','.join(sorted(map(self.ranges.encode_range, ranges_)))
