from __future__ import annotations

from collections.abc import Callable
from collections.abc import Mapping
from typing import Any
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core.traversal import visitors
from rmshared.content.taxonomy.core.traversal.abc import ILabels
from rmshared.content.taxonomy.core.traversal.abc import IRanges
from rmshared.content.taxonomy.core.traversal.abc import IFilters

Filter = TypeVar('Filter', bound=filters.Filter)


class Filters(IFilters[Filter]):
    def __init__(self, labels_: ILabels, ranges_: IRanges):
        self.labels = labels_
        self.ranges = ranges_
        self.filter_to_traverse_func_map: Mapping[Type[Filter], Callable[[Filter, Any], None]] = ensure_map_is_complete(filters.Filter, {
            filters.AnyLabel: self._traverse_any_label_filter,
            filters.NoLabels: self._traverse_no_labels_filter,
            filters.AnyRange: self._traverse_any_range_filter,
            filters.NoRanges: self._traverse_no_ranges_filter,
        })

    def traverse_filters(self, filters_, visitor) -> None:
        for filter_ in filters_:
            self._enter_filter(filter_, visitor=visitors.Filters(delegate=visitor))
            self._traverse_filter(filter_, visitor)
            self._leave_filter(filter_, visitor=visitors.Filters(delegate=visitor))

    @staticmethod
    def _enter_filter(filter_: Filter, visitor: visitors.IFilters) -> None:
        return visitor.enter_filter(filter_)

    @staticmethod
    def _leave_filter(filter_: Filter, visitor: visitors.IFilters) -> None:
        return visitor.leave_filter(filter_)

    def _traverse_filter(self, filter_: Filter, visitor: Any) -> None:
        self.filter_to_traverse_func_map[type(filter_)](filter_, visitor)

    def _traverse_any_label_filter(self, filter_: filters.AnyLabel, visitor: Any) -> None:
        self.labels.traverse_labels(filter_.labels, visitor)

    def _traverse_no_labels_filter(self, filter_: filters.NoLabels, visitor: Any) -> None:
        self.labels.traverse_labels(filter_.labels, visitor)

    def _traverse_any_range_filter(self, filter_: filters.AnyRange, visitor: Any) -> None:
        self.ranges.traverse_ranges(filter_.ranges, visitor)

    def _traverse_no_ranges_filter(self, filter_: filters.NoRanges, visitor: Any) -> None:
        self.ranges.traverse_ranges(filter_.ranges, visitor)
