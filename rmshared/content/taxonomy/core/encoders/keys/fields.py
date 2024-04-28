from typing import Callable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core.encoders.abc import IFields

Field = TypeVar('Field', bound=fields.Field)


class Fields(IFields[fields.Field, str]):
    def __init__(self):
        self.field_to_delegate_map: Mapping[Type[Field], Callable[[Field], str]] = ensure_map_is_complete(fields.Field, {
            fields.System: self._encode_system_field,
            fields.Custom: self._encode_custom_field,
        })

    def encode_field(self, field):
        return self.field_to_delegate_map[type(field)](field)

    @staticmethod
    def _encode_system_field(field: fields.System):
        return field.name

    @staticmethod
    def _encode_custom_field(field: fields.Custom):
        return f'{field.name}:{field.path}'
