from functools import cached_property
from operator import attrgetter
from typing import AbstractSet
from typing import Callable
from typing import Iterable
from typing import Mapping
from typing import Type

from rmshared.tools import group_to_mapping
from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy import filters
from rmshared.content.taxonomy.abc import Aspects
from rmshared.content.taxonomy.abc import Filter
from rmshared.content.taxonomy.abc import Scalar
from rmshared.content.taxonomy.abc import Label
from rmshared.content.taxonomy.abc import Range
from rmshared.content.taxonomy.abc import Value
from rmshared.content.taxonomy.abc import Field
from rmshared.content.taxonomy.abc import IMatcher


class Matcher(IMatcher):
    def __init__(self):
        self.filter_to_matcher_map: Mapping[Type[Filter], Callable[['Matcher.AspectsHolder', Filter], bool]] = ensure_map_is_complete(Filter, {
            filters.Phrase: self._do_aspects_match_phrase_filter,
            filters.AnyLabel: self._do_aspects_match_any_label_filter,
            filters.NoLabels: self._do_aspects_match_no_labels_filter,
            filters.AnyRange: self._do_aspects_match_any_range_filter,
            filters.NoRanges: self._do_aspects_match_no_ranges_filter,
        })

    def do_aspects_match_filters(self, aspects: Aspects, filters_: AbstractSet[Filter]) -> bool:
        return self._do_aspects_match_filters(self.AspectsHolder(aspects), filters_)

    def _do_aspects_match_filters(self, aspects: 'Matcher.AspectsHolder', filters_: AbstractSet[Filter]) -> bool:
        for filter_ in filters_:
            if not self._do_aspects_match_filter(aspects, filter_):
                return False
        else:
            return True

    def _do_aspects_match_filter(self, aspects: 'Matcher.AspectsHolder', filter_: Filter) -> bool:
        return self.filter_to_matcher_map[type(filter_)](aspects, filter_)

    def _do_aspects_match_phrase_filter(self, _aspects, _filter):
        raise NotImplementedError()

    def _do_aspects_match_any_label_filter(self, aspects: 'Matcher.AspectsHolder', filter_: filters.AnyLabel) -> bool:
        return self._do_aspects_match_any_label(aspects, filter_.labels) is True

    def _do_aspects_match_no_labels_filter(self, aspects: 'Matcher.AspectsHolder', filter_: filters.NoLabels) -> bool:
        return self._do_aspects_match_any_label(aspects, filter_.labels) is False

    @staticmethod
    def _do_aspects_match_any_label(aspects: 'Matcher.AspectsHolder', labels: Iterable[Label]) -> bool:
        return bool(frozenset(labels).intersection(aspects.labels))

    def _do_aspects_match_any_range_filter(self, aspects: 'Matcher.AspectsHolder', filter_: filters.AnyRange) -> bool:
        return self._do_aspects_match_any_range(aspects, filter_.ranges) is True

    def _do_aspects_match_no_ranges_filter(self, aspects: 'Matcher.AspectsHolder', filter_: filters.NoRanges) -> bool:
        return self._do_aspects_match_any_range(aspects, filter_.ranges) is False

    def _do_aspects_match_any_range(self, aspects: 'Matcher.AspectsHolder', ranges: Iterable[Range]) -> bool:
        return any(self._do_aspects_match_range(aspects, range_) for range_ in ranges)

    def _do_aspects_match_range(self, aspects: 'Matcher.AspectsHolder', range_: Range) -> bool:
        for value in aspects.get_values_by_field(range_.field):
            if self._does_value_match_range(value.value, range_):
                return True
        else:
            return False

    @staticmethod
    def _does_value_match_range(value: Scalar, range_: Range[Scalar]) -> bool:
        return all({
            range_.min_value is None or range_.min_value <= value,
            range_.max_value is None or range_.max_value >= value,
        })

    class AspectsHolder:
        def __init__(self, aspects: Aspects):
            self.aspects = aspects

        @property
        def labels(self) -> AbstractSet[Label]:
            return self.aspects.labels

        def get_values_by_field(self, field: Field) -> Iterable[Value]:
            return self.field_to_values_map.get(field) or []

        @cached_property
        def field_to_values_map(self) -> Mapping[Field, Iterable[Value]]:
            return group_to_mapping(self.aspects.values, key_func=attrgetter('field'))
