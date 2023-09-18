from abc import ABCMeta
from abc import abstractmethod
from typing import AbstractSet
from typing import Any
from typing import Generic
from typing import Mapping
from typing import Type

from rmshared.tools import dict_from_list
from rmshared.tools import ensure_map_is_complete
from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core.protocols.abc import Field
from rmshared.content.taxonomy.core.protocols.abc import IFields


class Fields(IFields[fields.Field]):
    def __init__(self):
        self.field_to_delegate_map: Mapping[Type[Field], 'Fields.IDelegate'] = ensure_map_is_complete(fields.Field, {
            fields.System: self.System(),
            fields.Custom: self.Custom(),
        })
        self.keys_to_delegate_map: Mapping[frozenset[str], 'Fields.IDelegate'] = dict_from_list(
            source=self.field_to_delegate_map.values(),
            key_func=self._get_delegate_keys,
        )

    @staticmethod
    def _get_delegate_keys(delegate: 'Fields.IDelegate') -> frozenset[str]:
        return frozenset(delegate.keys)

    def make_field(self, data):
        name, info = parse_name_and_info(data)
        keys = frozenset(dict(info).keys())
        return self.keys_to_delegate_map[keys].make_field(name, info)

    def jsonify_field(self, field):
        info = self.field_to_delegate_map[type(field)].jsonify_field_info(field)
        return {field.name: info}

    class IDelegate(Generic[Field], metaclass=ABCMeta):
        @property
        @abstractmethod
        def keys(self) -> AbstractSet[str]:
            pass

        @abstractmethod
        def make_field(self, name: str, info: Mapping[str, Any]) -> Field:
            pass

        @abstractmethod
        def jsonify_field_info(self, field: Field) -> Mapping[str, Any]:
            pass

    class System(IDelegate[fields.System]):
        @property
        def keys(self):
            return frozenset({})

        def make_field(self, name, info):
            assert info == dict()
            return fields.System(name=str(name))

        def jsonify_field_info(self, field: fields.System):
            return dict()

    class Custom(IDelegate[fields.Custom]):
        @property
        def keys(self):
            return frozenset({'path'})

        def make_field(self, name, info):
            return fields.Custom(name=str(name), path=str(info['path']))
    
        def jsonify_field_info(self, field: fields.Custom):
            return {'path': field.path}
