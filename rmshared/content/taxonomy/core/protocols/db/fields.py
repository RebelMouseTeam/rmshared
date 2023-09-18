from abc import ABCMeta
from abc import abstractmethod
from operator import attrgetter
from typing import Any
from typing import Generic
from typing import Mapping
from typing import Type

from rmshared.tools import dict_from_list
from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core.protocols.abc import Field
from rmshared.content.taxonomy.core.protocols.abc import IFields


class Fields(IFields[fields.Field]):
    def __init__(self):
        self.field_to_delegate_map: Mapping[Type[Field], 'Fields.IDelegate'] = ensure_map_is_complete(fields.Field, {
            fields.System: self.System(),
            fields.Custom: self.Custom(),
        })
        self.field_type_to_delegate_map: Mapping[str, 'Fields.IDelegate'] = dict_from_list(
            source=self.field_to_delegate_map.values(),
            key_func=attrgetter('type'),
        )

    def make_field(self, data):
        return self.field_type_to_delegate_map[str(data['type'])].make_field(dict(data['info']))

    def jsonify_field(self, field):
        delegate = self.field_to_delegate_map[type(field)]
        return {
            'type': delegate.type,
            'info': delegate.jsonify_field_info(field),
        }

    class IDelegate(Generic[Field], metaclass=ABCMeta):
        @property
        @abstractmethod
        def type(self) -> str:
            pass

        @abstractmethod
        def make_field(self, info: Mapping[str, Any]) -> Field:
            pass

        @abstractmethod
        def jsonify_field_info(self, field: Field) -> Mapping[str, Any]:
            pass

    class System(IDelegate[fields.System]):
        @property
        def type(self):
            return 'system'

        def make_field(self, info):
            return fields.System(name=str(info['name']))

        def jsonify_field_info(self, field: fields.System):
            return {'name': field.name}

    class Custom(IDelegate[fields.Custom]):
        @property
        def type(self):
            return 'custom'

        def make_field(self, info):
            return fields.Custom(name=str(info['name']), path=str(info['path']))

        def jsonify_field_info(self, field: fields.Custom):
            return {'name': field.name, 'path': field.path}
