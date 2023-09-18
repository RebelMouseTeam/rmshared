from abc import ABCMeta
from abc import abstractmethod
from typing import AbstractSet
from typing import Any
from typing import Generic
from typing import Mapping
from typing import Type

from rmshared.tools import dict_from_list
from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core.protocols.abc import Range
from rmshared.content.taxonomy.core.protocols.abc import IRanges
from rmshared.content.taxonomy.core.protocols.abc import IFields
from rmshared.content.taxonomy.core.protocols.abc import IValues


class Ranges(IRanges[ranges.Range]):
    def __init__(self, fields: IFields, values: IValues):
        self.range_to_delegate_map: Mapping[Type[Range], 'Ranges.IDelegate'] = ensure_map_is_complete(ranges.Range, {
            ranges.Between: self.Between(fields, values),
            ranges.LessThan: self.LessThan(fields, values),
            ranges.MoreThan: self.MoreThan(fields, values),
        })
        self.keys_to_delegate_map: Mapping[frozenset[str], 'Ranges.IDelegate'] = dict_from_list(
            source=self.range_to_delegate_map.values(),
            key_func=self._get_delegate_keys,
        )

    @staticmethod
    def _get_delegate_keys(delegate: 'Ranges.IDelegate') -> frozenset[str]:
        return frozenset(delegate.keys)

    def make_range(self, data):
        keys = frozenset(data.keys())
        return self.keys_to_delegate_map[keys].make_range(data)

    def jsonify_range(self, range_):
        return self.range_to_delegate_map[type(range_)].jsonify_range(range_)

    class IDelegate(Generic[Range], metaclass=ABCMeta):
        @property
        @abstractmethod
        def keys(self) -> AbstractSet[str]:
            pass

        @abstractmethod
        def make_range(self, data: Mapping[str, Any]) -> Range:
            pass

        @abstractmethod
        def jsonify_range(self, range_: Range) -> Mapping[str, Any]:
            pass

    class Between(IDelegate[ranges.Between]):
        def __init__(self, fields: IFields, values: IValues):
            self.fields = fields
            self.values = values

        @property
        def keys(self):
            return {'field', 'min', 'max'}

        def make_range(self, data):
            return ranges.Between(
                field=self.fields.make_field(data['field']),
                min_value=self.values.make_value(data['min']),
                max_value=self.values.make_value(data['max']),
            )

        def jsonify_range(self, range_: ranges.Between):
            return {
                'field': self.fields.jsonify_field(range_.field),
                'min': self.values.jsonify_value(range_.min_value),
                'max': self.values.jsonify_value(range_.max_value),
            }

    class LessThan(IDelegate[ranges.LessThan]):
        def __init__(self, fields: IFields, values: IValues):
            self.fields = fields
            self.values = values

        @property
        def keys(self):
            return {'field', 'max'}

        def make_range(self, data):
            return ranges.LessThan(
                field=self.fields.make_field(data['field']),
                value=self.values.make_value(data['max']),
            )

        def jsonify_range(self, range_: ranges.LessThan):
            return {
                'field': self.fields.jsonify_field(range_.field),
                'max': self.values.jsonify_value(range_.value),
            }

    class MoreThan(IDelegate[ranges.MoreThan]):
        def __init__(self, fields: IFields, values: IValues):
            self.fields = fields
            self.values = values

        @property
        def keys(self):
            return {'field', 'min'}

        def make_range(self, data):
            return ranges.MoreThan(
                field=self.fields.make_field(data['field']),
                value=self.values.make_value(data['min']),
            )

        def jsonify_range(self, range_: ranges.MoreThan):
            return {
                'field': self.fields.jsonify_field(range_.field),
                'min': self.values.jsonify_value(range_.value),
            }
