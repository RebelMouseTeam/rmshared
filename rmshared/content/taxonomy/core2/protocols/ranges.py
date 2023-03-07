from typing import Any
from typing import Callable
from typing import FrozenSet
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import filter_dict

from rmshared.content.taxonomy.core2 import ranges
from rmshared.content.taxonomy.core2.protocols.abc import IRanges
from rmshared.content.taxonomy.core2.protocols.abc import IFields
from rmshared.content.taxonomy.core2.protocols.abc import IValues


class Ranges(IRanges[ranges.Range]):
    R = TypeVar('R', bound=ranges.Range)
    KEYS = frozenset({'min', 'max'})

    def __init__(self, fields: IFields, values: IValues):
        self.fields = fields
        self.values = values
        self.range_keys_to_factory_func_map: Mapping[FrozenSet[str], Callable[[Mapping[str, Any]], ranges.Range]] = {
            frozenset({'max'}): self._make_less_than_range,
            frozenset({'min'}): self._make_more_than_range,
            frozenset({'min', 'max'}): self._make_between_range,
        }
        self.range_to_jsonify_func_map: Mapping[Type[ranges.Range], Callable[[Ranges.R], Mapping[str, Any]]] = {
            ranges.LessThan: self._jsonify_less_than_range,
            ranges.MoreThan: self._jsonify_more_than_range,
            ranges.Between: self._jsonify_between_range,
        }

    def make_range(self, data):
        keys = frozenset(filter_dict(data, value_func=lambda _: _ is not None).keys())
        keys = keys.intersection(self.KEYS)
        return self.range_keys_to_factory_func_map[keys](data)

    def jsonify_range(self, range_):
        return self.range_to_jsonify_func_map[type(range_)](range_)

    def _make_less_than_range(self, data: Mapping[str, Any]) -> ranges.LessThan:
        return ranges.LessThan(
            field=self.fields.make_field(data['field']),
            value=self.values.make_value(data['max']),
        )

    def _jsonify_less_than_range(self, range_: ranges.LessThan) -> Mapping[str, Any]:
        return {
            'field': self.fields.jsonify_field(range_.field),
            'max': self.values.jsonify_value(range_.value),
        }

    def _make_more_than_range(self, data: Mapping[str, Any]) -> ranges.MoreThan:
        return ranges.MoreThan(
            field=self.fields.make_field(data['field']),
            value=self.values.make_value(data['min']),
        )

    def _jsonify_more_than_range(self, range_: ranges.MoreThan) -> Mapping[str, Any]:
        return {
            'field': self.fields.jsonify_field(range_.field),
            'min': self.values.jsonify_value(range_.value),
        }

    def _make_between_range(self, data: Mapping[str, Any]) -> ranges.Between:
        return ranges.Between(
            field=self.fields.make_field(data['field']),
            min_value=self.values.make_value(data['min']),
            max_value=self.values.make_value(data['max']),
        )

    def _jsonify_between_range(self, range_: ranges.Between) -> Mapping[str, Any]:
        return {
            'field': self.fields.jsonify_field(range_.field),
            'min': self.values.jsonify_value(range_.min_value),
            'max': self.values.jsonify_value(range_.max_value),
        }
