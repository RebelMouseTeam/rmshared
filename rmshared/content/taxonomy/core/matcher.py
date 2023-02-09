from typing import Callable
from typing import Iterable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core.abc import Filter
from rmshared.content.taxonomy.core.abc import Label
from rmshared.content.taxonomy.core.abc import Range
from rmshared.content.taxonomy.core.abc import Value
from rmshared.content.taxonomy.core.abc import IMatcher


class Matcher(IMatcher):
    Filter = TypeVar('Filter', bound=Filter)
    Range = TypeVar('Range', bound=Range)

    def __init__(self):
        self.filter_to_matcher_map: Mapping[Type[Filter], Callable[['Matcher.IAspects', 'Matcher.Filter'], bool]] = {
            filters.AnyLabel: self._do_aspects_match_any_label_filter,
            filters.NoLabels: self._do_aspects_match_no_labels_filter,
            filters.AnyRange: self._do_aspects_match_any_range_filter,
            filters.NoRanges: self._do_aspects_match_no_ranges_filter,
        }
        self.range_to_matcher_map: Mapping[Type[Range], Callable[['Value', 'Matcher.Range'], bool]] = {
            ranges.Between: self._does_value_match_between_range,
            ranges.LessThan: self._does_value_match_less_than_range,
            ranges.MoreThan: self._does_value_match_more_than_range,
        }

    def do_aspects_match_filters(self, aspects, filters_):
        return self._do_aspects_match_filters(aspects, filters_)

    def _do_aspects_match_filters(self, aspects: 'Matcher.IAspects', filters_: Iterable[Filter]) -> bool:
        for filter_ in filters_:
            if not self._do_aspects_match_filter(aspects, filter_):
                return False
        else:
            return True

    def _do_aspects_match_filter(self, aspects: 'Matcher.IAspects', filter_: Filter) -> bool:
        return self.filter_to_matcher_map[type(filter_)](aspects, filter_)

    def _do_aspects_match_any_label_filter(self, aspects: 'Matcher.IAspects', filter_: filters.AnyLabel) -> bool:
        return self._do_aspects_match_any_label(aspects, filter_.labels) is True

    def _do_aspects_match_no_labels_filter(self, aspects: 'Matcher.IAspects', filter_: filters.NoLabels) -> bool:
        return self._do_aspects_match_any_label(aspects, filter_.labels) is False

    @staticmethod
    def _do_aspects_match_any_label(aspects: 'Matcher.IAspects', labels: Iterable[Label]) -> bool:
        return bool(frozenset(labels).intersection(aspects.labels))

    def _do_aspects_match_any_range_filter(self, aspects: 'Matcher.IAspects', filter_: filters.AnyRange) -> bool:
        return self._do_aspects_match_any_range(aspects, filter_.ranges) is True

    def _do_aspects_match_no_ranges_filter(self, aspects: 'Matcher.IAspects', filter_: filters.NoRanges) -> bool:
        return self._do_aspects_match_any_range(aspects, filter_.ranges) is False

    def _do_aspects_match_any_range(self, aspects: 'Matcher.IAspects', ranges_: Iterable[Range]) -> bool:
        return any(self._do_aspects_match_range(aspects, range_) for range_ in ranges_)

    def _do_aspects_match_range(self, aspects: 'Matcher.IAspects', range_: Range) -> bool:
        for value in aspects.values:
            if self._does_value_match_range(value, range_):
                return True
        else:
            return False

    def _does_value_match_range(self, value: 'Value', range_: Range) -> bool:
        return self.range_to_matcher_map[type(range_)](value, range_)

    @staticmethod
    def _does_value_match_between_range(value: 'Value', range_: ranges.Between) -> bool:
        return value.field == range_.field and range_.min_value <= value.value <= range_.max_value

    @staticmethod
    def _does_value_match_less_than_range(value: 'Value', range_: ranges.LessThan) -> bool:
        return value.field == range_.field and value.value <= range_.value

    @staticmethod
    def _does_value_match_more_than_range(value: 'Value', range_: ranges.MoreThan) -> bool:
        return value.field == range_.field and value.value >= range_.value
