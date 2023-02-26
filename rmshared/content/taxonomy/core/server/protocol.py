from typing import AbstractSet
from typing import Any
from typing import Callable
from typing import FrozenSet
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import Sequence
from typing import Type
from typing import TypeVar

from rmshared.tools import filter_dict
from rmshared.tools import invert_dict
from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import orders
from rmshared.content.taxonomy.core import fields
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

    def jsonify_filters(self, filters):
        return map(self.filters.jsonify_filter, filters)

    def make_order(self, data):
        return self.orders.make_order(data)

    def make_field(self, data):
        return self.fields.make_field(data)

    class Filters:
        F = TypeVar('F', bound=Filter)

        """
        TODO:
            {'phrase': {'phrase': 'Hello', 'syntax': {'any': {'thing': 'here'}}}},
            {'phrase': {'phrase': 'World', 'weights': ['10', '0', '4']}},
        """

        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.filter_to_filter_name_map: Mapping[Type[Filter], str] = {
                filters.AnyLabel: 'any_label',
                filters.NoLabels: 'no_labels',
                filters.AnyRange: 'any_range',
                filters.NoRanges: 'no_ranges',
            }
            self.filter_name_to_filter_map: Mapping[str, Type[Filter]] = invert_dict(self.filter_to_filter_name_map)
            self.filter_to_factory_func_map: Mapping[Type[Filter], Callable[[Any], Filter]] = {
                filters.AnyLabel: self._make_any_label_filter,
                filters.NoLabels: self._make_no_labels_filter,
                filters.AnyRange: self._make_any_range_filter,
                filters.NoRanges: self._make_no_ranges_filter,
            }
            self.filter_to_jsonify_func_map: Mapping[Type[Filter], Callable[[Protocol.Filters.F], Sequence[Mapping[str, Any]]]] = {
                filters.AnyLabel: self._jsonify_labels_filter_info,
                filters.NoLabels: self._jsonify_labels_filter_info,
                filters.AnyRange: self._jsonify_ranges_filter_info,
                filters.NoRanges: self._jsonify_ranges_filter_info,
            }

        def make_filter(self, data: Mapping[str, Any]) -> Filter:
            name, info = parse_name_and_info(data)
            filter_type = self.filter_name_to_filter_map[name]
            return self.filter_to_factory_func_map[filter_type](info)

        def jsonify_filter(self, filter_: Filter) -> Mapping[str, Any]:
            name = self.filter_to_filter_name_map[type(filter_)]
            info = self.filter_to_jsonify_func_map[type(filter_)](filter_)
            return {name: info}

        def _make_any_label_filter(self, data: Any):
            return filters.AnyLabel(labels=tuple(self.protocol.labels.stream_labels(data)))

        def _make_no_labels_filter(self, data: Any):
            return filters.NoLabels(labels=tuple(self.protocol.labels.stream_labels(data)))

        def _jsonify_labels_filter_info(self, filter_: filters.AnyLabel | filters.NoLabels) -> Sequence[Mapping[str, Any]]:
            return list(map(self.protocol.labels.jsonify_label, filter_.labels))

        def _make_any_range_filter(self, data: Any):
            return filters.AnyRange(ranges=tuple(self.protocol.ranges.stream_ranges(data)))

        def _make_no_ranges_filter(self, data: Any):
            return filters.NoRanges(ranges=tuple(self.protocol.ranges.stream_ranges(data)))

        def _jsonify_ranges_filter_info(self, filter_: filters.AnyRange | filters.NoRanges) -> Sequence[Mapping[str, Any]]:
            return list(map(self.protocol.ranges.jsonify_range, filter_.ranges))

    class Orders:
        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol

        def make_order(self, data: Mapping[str, Any]) -> orders.Value:
            return orders.Value(
                field=self.protocol.fields.make_field(data['field']),
                reverse=bool(data['reverse']),
            )

    class Labels:
        L = TypeVar('L', bound=Label)

        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.label_to_label_name_map: Mapping[Type[Label], str] = {
                labels.Value: 'value',
                labels.Badge: 'badge',
                labels.Empty: 'empty',
            }
            self.label_name_to_label_map: Mapping[str, Type[Label]] = invert_dict(self.label_to_label_name_map)
            self.label_to_factory_func_map: Mapping[Type[Label], Callable[[Mapping[str, Any]], Label]] = {
                labels.Value: self._make_value_label,
                labels.Badge: self._make_badge_label,
                labels.Empty: self._make_empty_label,
            }
            self.label_to_jsonify_func_map: Mapping[Type[Label], Callable[[Protocol.Labels.L], Mapping[str, Any]]] = {
                labels.Value: self._jsonify_value_label_info,
                labels.Badge: self._jsonify_badge_label_info,
                labels.Empty: self._jsonify_empty_label_info,
            }

        def stream_labels(self, data: Iterable[Mapping[str, Any]]) -> Iterator[Label]:
            return map(self._make_label, data)

        def _make_label(self, data: Mapping[str, Any]) -> Label:
            name, info = parse_name_and_info(data)
            label_type = self.label_name_to_label_map[name]
            return self.label_to_factory_func_map[label_type](info)

        def jsonify_label(self, label: Label) -> Mapping[str, Any]:
            name = self.label_to_label_name_map[type(label)]
            info = self.label_to_jsonify_func_map[type(label)](label)
            return {name: info}

        def _make_value_label(self, info: Mapping[str, Any]):
            return labels.Value(self.protocol.fields.make_field(info['field']), value=info['value'])

        def _jsonify_value_label_info(self, label: labels.Value) -> Mapping[str, Any]:
            return {
                'field': self.protocol.fields.jsonify_field(label.field),
                'value': label.value,
            }

        def _make_badge_label(self, info: Mapping[str, Any]):
            return labels.Badge(self.protocol.fields.make_field(info['field']))

        def _jsonify_badge_label_info(self, label: labels.Badge) -> Mapping[str, Any]:
            return {
                'field': self.protocol.fields.jsonify_field(label.field),
            }

        def _make_empty_label(self, info: Mapping[str, Any]):
            return labels.Empty(self.protocol.fields.make_field(info['field']))

        def _jsonify_empty_label_info(self, label: labels.Empty) -> Mapping[str, Any]:
            return {
                'field': self.protocol.fields.jsonify_field(label.field),
            }

    class Ranges:
        R = TypeVar('R', bound=Range)
        KEYS = frozenset({'min', 'max'})

        def __init__(self, protocol: 'Protocol'):
            self.protocol = protocol
            self.range_keys_to_factory_func_map: Mapping[FrozenSet[str], Callable[[Mapping[str, Any]], Range]] = {
                frozenset({'max'}): self._make_less_than_range,
                frozenset({'min'}): self._make_more_than_range,
                frozenset({'min', 'max'}): self._make_between_range,
            }
            self.range_to_jsonify_func_map: Mapping[Type[Range], Callable[[Protocol.Ranges.R], Mapping[str, Any]]] = {
                ranges.LessThan: self._jsonify_less_than_range,
                ranges.MoreThan: self._jsonify_more_than_range,
                ranges.Between: self._jsonify_between_range,
            }

        def stream_ranges(self, data: Iterable[Mapping[str, Any]]) -> Iterator[Range]:
            return map(self._make_range, data)

        def _make_range(self, data: Mapping[str, Any]) -> Range:
            keys = frozenset(filter_dict(data, value_func=lambda _: _ is not None).keys())
            keys = keys.intersection(self.KEYS)
            return self.range_keys_to_factory_func_map[keys](data)

        def jsonify_range(self, range_: Range) -> Mapping[str, Any]:
            return self.range_to_jsonify_func_map[type(range_)](range_)

        def _make_less_than_range(self, data: Mapping[str, Any]) -> ranges.LessThan:
            return ranges.LessThan(
                field=self.protocol.fields.make_field(data['field']),
                value=data['max'],
            )

        def _jsonify_less_than_range(self, range_: ranges.LessThan) -> Mapping[str, Any]:
            return {
                'field': self.protocol.fields.jsonify_field(range_.field),
                'max': range_.value,
            }

        def _make_more_than_range(self, data: Mapping[str, Any]) -> ranges.MoreThan:
            return ranges.MoreThan(
                field=self.protocol.fields.make_field(data['field']),
                value=data['min'],
            )

        def _jsonify_more_than_range(self, range_: ranges.MoreThan) -> Mapping[str, Any]:
            return {
                'field': self.protocol.fields.jsonify_field(range_.field),
                'min': range_.value,
            }

        def _make_between_range(self, data: Mapping[str, Any]) -> ranges.Between:
            return ranges.Between(
                field=self.protocol.fields.make_field(data['field']),
                min_value=data['min'],
                max_value=data['max'],
            )

        def _jsonify_between_range(self, range_: ranges.Between) -> Mapping[str, Any]:
            return {
                'field': self.protocol.fields.jsonify_field(range_.field),
                'min': range_.min_value,
                'max': range_.max_value,
            }

    class Fields:
        F = TypeVar('F', bound=Field)

        def __init__(self):
            self.field_keys_to_factory_func_map: Mapping[AbstractSet[str], Callable[[str, Mapping[str, Any]], Field]] = {
                frozenset(): self._make_system_field,
                frozenset({'path'}): self._make_custom_field,
            }
            self.field_to_jsonify_func_map: Mapping[Type[Field], Callable[[Protocol.Fields.F], Mapping[str, Any]]] = {
                fields.System: self._jsonify_system_field,
                fields.Custom: self._jsonify_custom_field,
            }

        def make_field(self, data: Mapping[str, Any]) -> Field:
            name, info = parse_name_and_info(data)
            keys = frozenset(info.keys())
            return self.field_keys_to_factory_func_map[keys](name, info)

        def jsonify_field(self, field: Field) -> Mapping[str, Any]:
            return self.field_to_jsonify_func_map[type(field)](field)

        @staticmethod
        def _make_system_field(name: str, _data: Mapping[str, Any]) -> fields.System:
            return fields.System(name)

        @staticmethod
        def _jsonify_system_field(field: fields.System) -> Mapping[str, Any]:
            return {field.name: {}}

        @staticmethod
        def _make_custom_field(name: str, data: Mapping[str, Any]) -> fields.Custom:
            return fields.Custom(name, path=str(data['path']))

        @staticmethod
        def _jsonify_custom_field(field: fields.Custom) -> Mapping[str, Any]:
            return {field.name: {'path': field.path}}
