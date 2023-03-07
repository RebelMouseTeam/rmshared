from typing import AbstractSet
from typing import Any
from typing import Callable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.core2 import fields
from rmshared.content.taxonomy.core2.protocols.abc import IFields


class Fields(IFields[fields.Field]):
    F = TypeVar('F', bound=fields.Field)
    KEYS = frozenset({'path'})

    def __init__(self):
        self.field_keys_to_factory_func_map: Mapping[AbstractSet[str], Callable[[str, Mapping[str, Any]], fields.Field]] = {
            frozenset(): self._make_system_field,
            frozenset({'path'}): self._make_custom_field,
        }
        self.field_to_jsonify_func_map: Mapping[Type[fields.Field], Callable[[Fields.F], Mapping[str, Any]]] = {
            fields.System: self._jsonify_system_field,
            fields.Custom: self._jsonify_custom_field,
        }

    def make_field(self, data):
        name, info = parse_name_and_info(data)
        keys = frozenset(info.keys())
        keys = keys.intersection(self.KEYS)
        return self.field_keys_to_factory_func_map[keys](name, info)

    def jsonify_field(self, field):
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
