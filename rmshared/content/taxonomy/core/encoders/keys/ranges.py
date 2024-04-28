from typing import Callable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core.encoders.abc import IFields
from rmshared.content.taxonomy.core.encoders.abc import IRanges
from rmshared.content.taxonomy.core.encoders.abc import IValues

Range = TypeVar('Range', bound=ranges.Range)


class Ranges(IRanges[ranges.Range, str]):
    def __init__(self, fields: IFields, values: IValues):
        self.fields = fields
        self.values = values
        self.range_to_delegate_map: Mapping[Type[Range], Callable[[Range], str]] = ensure_map_is_complete(ranges.Range, {
            ranges.Between: self._encode_between_range,
            ranges.LessThan: self._encode_less_than_range,
            ranges.MoreThan: self._encode_more_than_range,
        })

    def encode_range(self, range_):
        return self.range_to_delegate_map[type(range_)](range_)

    def _encode_between_range(self, range_: ranges.Between):
        field = self.fields.encode_field(range_.field)
        min_value = self.values.encode_value(range_.min_value)
        max_value = self.values.encode_value(range_.max_value)
        return f'{min_value}<{field}<{max_value}'

    def _encode_less_than_range(self, range_: ranges.LessThan):
        field = self.fields.encode_field(range_.field)
        value = self.values.encode_value(range_.value)
        return f'{field}<{value}'

    def _encode_more_than_range(self, range_: ranges.MoreThan):
        field = self.fields.encode_field(range_.field)
        value = self.values.encode_value(range_.value)
        return f'{value}<{field}'
