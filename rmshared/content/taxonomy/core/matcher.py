from typing import Any
from typing import Callable
from typing import Iterable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges

from rmshared.content.taxonomy.core.abc import IEntity
from rmshared.content.taxonomy.core.abc import IMatcher

Filter = TypeVar('Filter', bound=filters.Filter)
Label = TypeVar('Label', bound=labels.Label)
Range = TypeVar('Range', bound=ranges.Range)
Value = TypeVar('Value')


class Matcher(IMatcher):
    def __init__(self):
        self.filter_to_matcher_map: Mapping[Type[filters.Filter], Callable[[IEntity, Filter], bool]] = {
            filters.AnyLabel: self._does_entity_match_any_label_filter,
            filters.NoLabels: self._does_entity_match_no_labels_filter,
            filters.AnyRange: self._does_entity_match_any_range_filter,
            filters.NoRanges: self._does_entity_match_no_ranges_filter,
        }
        self.label_to_matcher_map: Mapping[Type[labels.Label], Callable[[IEntity, Label], bool]] = {
            labels.Value: self._does_entity_match_value_label,
            labels.Badge: self._does_entity_match_badge_label,
            labels.Empty: self._does_entity_match_empty_label,
        }
        self.range_to_matcher_map: Mapping[Type[ranges.Range], Callable[[Value, Range], bool]] = {
            ranges.Between: self._does_value_match_between_range,
            ranges.LessThan: self._does_value_match_less_than_range,
            ranges.MoreThan: self._does_value_match_more_than_range,
        }

    def does_entity_match_filters(self, entity, filters_):
        return self._does_entity_match_filters(entity, filters_)

    def _does_entity_match_filters(self, entity: IEntity, filters_: Iterable[Filter]) -> bool:
        for filter_ in filters_:
            if not self._does_entity_match_filter(entity, filter_):
                return False
        else:
            return True

    def _does_entity_match_filter(self, entity: IEntity, filter_: Filter) -> bool:
        return self.filter_to_matcher_map[type(filter_)](entity, filter_)

    def _does_entity_match_any_label_filter(self, entity: IEntity, filter_: filters.AnyLabel) -> bool:
        return self._does_entity_match_any_label(entity, filter_.labels) is True

    def _does_entity_match_no_labels_filter(self, entity: IEntity, filter_: filters.NoLabels) -> bool:
        return self._does_entity_match_any_label(entity, filter_.labels) is False

    def _does_entity_match_any_label(self, entity: IEntity, labels_: Iterable[labels.Label]) -> bool:
        for label in labels_:
            if self._does_entity_match_label(entity, label):
                return True
        else:
            return False

    def _does_entity_match_label(self, entity: IEntity, label: labels.Label) -> bool:
        return self.label_to_matcher_map[type(label)](entity, label)

    @staticmethod
    def _does_entity_match_value_label(entity: IEntity, label: labels.Value) -> bool:
        return label.value in entity.get_values(label.field)

    @staticmethod
    def _does_entity_match_badge_label(entity: IEntity, label: labels.Badge) -> bool:
        return True in entity.get_values(label.field)

    @staticmethod
    def _does_entity_match_empty_label(entity: IEntity, label: labels.Empty) -> bool:
        return len(entity.get_values(label.field)) == 0

    def _does_entity_match_any_range_filter(self, entity: IEntity, filter_: filters.AnyRange) -> bool:
        return self._does_entity_match_any_range(entity, filter_.ranges) is True

    def _does_entity_match_no_ranges_filter(self, entity: IEntity, filter_: filters.NoRanges) -> bool:
        return self._does_entity_match_any_range(entity, filter_.ranges) is False

    def _does_entity_match_any_range(self, entity: IEntity, ranges_: Iterable[ranges.Range]) -> bool:
        for range_ in ranges_:
            for value in entity.get_values(range_.field):
                if self._does_value_match_range(value, range_):
                    return True
        else:
            return False

    def _does_value_match_range(self, entity: IEntity, range_: ranges.Range) -> bool:
        return self.range_to_matcher_map[type(range_)](entity, range_)

    @staticmethod
    def _does_value_match_between_range(value: Value, range_: ranges.Between[Any, Value]) -> bool:
        return range_.min_value <= value <= range_.max_value

    @staticmethod
    def _does_value_match_less_than_range(value: Value, range_: ranges.LessThan[Any, Value]) -> bool:
        return value <= range_.value

    @staticmethod
    def _does_value_match_more_than_range(value: Value, range_: ranges.MoreThan[Any, Value]) -> bool:
        return value >= range_.value
