from collections.abc import Callable
from collections.abc import Mapping
from contextlib import AbstractContextManager
from typing import Any
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_context_manager
from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core.traversal import visitors
from rmshared.content.taxonomy.core.traversal.abc import IRanges

Range = TypeVar('Range', bound=ranges.Range)


class Ranges(IRanges[Range]):
    def __init__(self):
        self.range_to_traverse_func_map: Mapping[Type[Range], Callable[[Range, Any], None]] = ensure_map_is_complete(ranges.Range, {
            ranges.Between: self._traverse_between_range,
            ranges.MoreThan: self._traverse_more_than_range,
            ranges.LessThan: self._traverse_less_than_range,
        })

    def traverse_ranges(self, ranges_, visitor) -> None:
        for range_ in ranges_:
            with self._visit_range(range_, visitor=visitors.Ranges(delegate=visitor)):
                self._traverse_range(range_, visitor)

    @staticmethod
    def _visit_range(range_: Range, visitor: visitors.IRanges) -> AbstractContextManager[None]:
        return ensure_context_manager(delegate=visitor.visit_range(range_))

    def _traverse_range(self, range_: Range, visitor: Any) -> None:
        self.range_to_traverse_func_map[type(range_)](range_, visitor)

    def _traverse_between_range(self, range_: ranges.Between, visitor: Any) -> None:
        self._visit_field(range_.field, visitor=visitors.Fields(delegate=visitor))
        self._visit_value(range_.min_value, visitor=visitors.Values(delegate=visitor))
        self._visit_value(range_.max_value, visitor=visitors.Values(delegate=visitor))

    def _traverse_more_than_range(self, range_: ranges.MoreThan, visitor: Any) -> None:
        self._visit_field(range_.field, visitor=visitors.Fields(delegate=visitor))
        self._visit_value(range_.value, visitor=visitors.Values(delegate=visitor))

    def _traverse_less_than_range(self, range_: ranges.LessThan, visitor: Any) -> None:
        self._visit_field(range_.field, visitor=visitors.Fields(delegate=visitor))
        self._visit_value(range_.value, visitor=visitors.Values(delegate=visitor))

    @staticmethod
    def _visit_field(field, visitor: visitors.IFields) -> None:
        return visitor.visit_field(field)

    @staticmethod
    def _visit_value(value, visitor: visitors.IValues) -> None:
        return visitor.visit_value(value)
