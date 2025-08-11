from __future__ import annotations

from collections.abc import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.sql import compiling

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core.sql.compiling.abc import IFilters
from rmshared.content.taxonomy.core.sql.compiling.abc import IRanges
from rmshared.content.taxonomy.core.sql.compiling.abc import ILabels

F = TypeVar('F', bound=filters.Filter)


class Filters(IFilters[filters.Filter]):
    def __init__(self, labels_: ILabels, ranges_: IRanges):
        self.labels_ = labels_
        self.ranges_ = ranges_
        self.filter_to_make_tree_func_map: Mapping[Type[F], compiling.MakeTreeFunc[F]] = ensure_map_is_complete(filters.Filter, {
            filters.AnyLabel: self._make_tree_from_any_label_filter,
            filters.NoLabels: self._make_tree_from_no_labels_filter,
            filters.AnyRange: self._make_tree_from_any_range_filter,
            filters.NoRanges: self._make_tree_from_no_ranges_filter,
        })

    def make_tree_from_filter(self, filter_: filters.Filter):
        return self.filter_to_make_tree_func_map[type(filter_)](filter_)

    def _make_tree_from_any_label_filter(self, filter_: filters.AnyLabel) -> compiling.ITree:
        return self.labels_.make_tree_from_labels(filter_.labels, matcher=self.labels_.Match())

    def _make_tree_from_no_labels_filter(self, filter_: filters.NoLabels) -> compiling.ITree:
        return self.labels_.make_tree_from_labels(filter_.labels, matcher=self.labels_.MatchNot())

    def _make_tree_from_any_range_filter(self, filter_: filters.AnyRange) -> compiling.ITree:
        return self.ranges_.make_tree_from_ranges(filter_.ranges, matcher=self.ranges_.Match())

    def _make_tree_from_no_ranges_filter(self, filter_: filters.NoRanges) -> compiling.ITree:
        return self.ranges_.make_tree_from_ranges(filter_.ranges, matcher=self.ranges_.MatchNot())
