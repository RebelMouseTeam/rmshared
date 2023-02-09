from typing import Any
from typing import Callable
from typing import FrozenSet
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import Type

from rmshared.tools import filter_dict
from rmshared.tools import invert_dict
from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import orders
from rmshared.content.taxonomy.core.abc import Field
from rmshared.content.taxonomy.core.abc import Label
from rmshared.content.taxonomy.core.abc import Range
from rmshared.content.taxonomy.core.abc import Filter
from rmshared.content.taxonomy.core.server.abc import IProtocol


class Protocol(IProtocol):
    def __init__(self):
        self.filters = self.Filters(self)
        self.orders = self.Orders(self)
        self.labels = self.Labels(self)
        self.ranges = self.Ranges(self)
        self.fields = self.Fields()

    def make_filters(self, data):
        return map(self.filters.make_filter, data)

    def make_order(self, data):
        return self.orders.make_order(data)

    class Filters:
        """
        TODO:
            {'phrase': {'phrase': 'Hello', 'syntax': {'any': {'thing': 'here'}}}},
            {'phrase': {'phrase': 'World', 'weights': ['10', '0', '4']}},
        """

        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.filter_name_to_filter_map: Mapping[str, Type[Filter]] = invert_dict({
                filters.AnyLabel: 'any_label',
                filters.NoLabels: 'no_labels',
                filters.AnyRange: 'any_range',
                filters.NoRanges: 'no_ranges',
            })
            self.filter_to_factory_func_map: Mapping[Type[Filter], Callable[[Any], Filter]] = {
                filters.AnyLabel: self._make_any_label_filter,
                filters.NoLabels: self._make_no_labels_filter,
                filters.AnyRange: self._make_any_range_filter,
                filters.NoRanges: self._make_no_ranges_filter,
            }

        def make_filter(self, data: Mapping[str, Any]) -> Filter:
            name, info = parse_name_and_info(data)
            filter_type = self.filter_name_to_filter_map[name]
            return self.filter_to_factory_func_map[filter_type](info)

        def _make_any_label_filter(self, data: Any):
            return filters.AnyLabel(labels=tuple(self.protocol.labels.stream_labels(data)))

        def _make_no_labels_filter(self, data: Any):
            return filters.NoLabels(labels=tuple(self.protocol.labels.stream_labels(data)))

        def _make_any_range_filter(self, data: Any):
            return filters.AnyRange(ranges=tuple(self.protocol.ranges.stream_ranges(data)))

        def _make_no_ranges_filter(self, data: Any):
            return filters.NoRanges(ranges=tuple(self.protocol.ranges.stream_ranges(data)))

    class Orders:
        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol

        def make_order(self, data: Mapping[str, Any]) -> orders.Value:
            return orders.Value(
                field=self.protocol.fields.make_field(data['field']),
                reverse=bool(data['reverse']),
            )

    class Labels:
        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.label_name_to_label_map: Mapping[str, Type[Label]] = invert_dict({
                labels.Value: 'value',
                labels.Badge: 'badge',
                labels.Empty: 'empty',
            })
            self.label_to_factory_func_map: Mapping[Type[Label], Callable[[Mapping[str, Any]], Label]] = {
                labels.Value: self._make_value_label,
                labels.Badge: self._make_badge_label,
                labels.Empty: self._make_empty_label,
            }

        def stream_labels(self, data: Iterable[Mapping[str, Any]]) -> Iterator[Label]:
            return map(self._make_label, data)

        def _make_label(self, data: Mapping[str, Any]) -> Label:
            name, info = parse_name_and_info(data)
            label_type = self.label_name_to_label_map[name]
            return self.label_to_factory_func_map[label_type](info)

        def _make_value_label(self, info: Mapping[str, Any]):
            return labels.Value(self.protocol.fields.make_field(info['field']), value=info['value'])

        def _make_badge_label(self, info: Mapping[str, Any]):
            return labels.Badge(self.protocol.fields.make_field(info['field']))

        def _make_empty_label(self, info: Mapping[str, Any]):
            return labels.Empty(self.protocol.fields.make_field(info['field']))

    class Ranges:
        FIELDS = frozenset({'min', 'max'})

        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.fields_to_factory_func_map: Mapping[FrozenSet[str], Callable[[Mapping[str, Any]], Range]] = {
                frozenset({'max'}): self._make_less_than_range,
                frozenset({'min'}): self._make_more_than_range,
                frozenset({'min', 'max'}): self._make_between_range,
            }

        def stream_ranges(self, data: Iterable[Mapping[str, Any]]) -> Iterator[Range]:
            return map(self._make_range, data)

        def _make_range(self, data: Mapping[str, Any]) -> Range:
            fields = frozenset(filter_dict(data, value_func=lambda _: _ is not None).keys())
            fields = fields.intersection(self.FIELDS)
            return self.fields_to_factory_func_map[fields](data)

        def _make_less_than_range(self, data: Mapping[str, Any]) -> ranges.LessThan:
            return ranges.LessThan(
                field=self.protocol.fields.make_field(data['field']),
                value=data['max'],
            )

        def _make_more_than_range(self, data: Mapping[str, Any]) -> ranges.MoreThan:
            return ranges.MoreThan(
                field=self.protocol.fields.make_field(data['field']),
                value=data['min'],
            )

        def _make_between_range(self, data: Mapping[str, Any]) -> ranges.Between:
            return ranges.Between(
                field=self.protocol.fields.make_field(data['field']),
                min_value=data['min'],
                max_value=data['max'],
            )

    class Fields:
        @staticmethod
        def make_field(data: Mapping[str, Any]) -> Field:
            name, _ = parse_name_and_info(data)
            return Field(name)
