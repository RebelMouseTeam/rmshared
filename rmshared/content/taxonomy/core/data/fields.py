from typing import Any
from typing import Callable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import invert_dict
from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core.data.abc import IFields

Field = TypeVar('Field', bound=fields.Field)


class Fields(IFields):
    def __init__(self):
        self.field_to_type_map: Mapping[Type[Field], str] = ensure_map_is_complete(fields.Field, {
            fields.System: 'system',
            fields.Custom: 'custom',
        })
        self.field_from_type_map: Mapping[str, Type[Field]] = invert_dict(self.field_to_type_map)
        self.field_to_info_func_map: Mapping[Type[Field], Callable[[Field], dict]] = ensure_map_is_complete(fields.Field, {
            fields.System: self._make_system_field_info,
            fields.Custom: self._make_custom_field_info,
        })
        self.field_to_factory_func_map: Mapping[Type[Field], Callable[[Any], Field]] = ensure_map_is_complete(fields.Field, {
            fields.System: lambda _: dict(),
            fields.Custom: self._make_custom_field,
        })

    def make_field_data(self, field: fields.Field) -> Mapping[str, Any]:
        return {
            'type': self.field_to_type_map[type(field)],
            'info': self.field_to_info_func_map[type(field)](field),
        }

    def make_field(self, data: Mapping[str, Any]) -> fields.Field:
        return self.field_to_factory_func_map[self.field_from_type_map[data['type']]](data['info'])

    @staticmethod
    def _make_system_field_info(field: fields.System) -> Mapping[str, Any]:
        return {'name': field.name}

    @staticmethod
    def _make_system_field(data: Mapping[str, Any]) -> fields.System:
        return fields.System(name=str(data['name']))

    @staticmethod
    def _make_custom_field_info(field: fields.Custom) -> Mapping[str, Any]:
        return {'name': field.name, 'path': field.path}

    @staticmethod
    def _make_custom_field(data: Mapping[str, Any]) -> fields.Custom:
        return fields.Custom(name=str(data['name']), path=str(data['path']))
