from abc import ABCMeta
from abc import abstractmethod
from operator import attrgetter
from typing import AbstractSet
from typing import Any
from typing import Generic
from typing import Mapping
from typing import Type

from rmshared.tools import dict_from_list
from rmshared.tools import ensure_map_is_complete
from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core.protocols.abc import Label
from rmshared.content.taxonomy.core.protocols.abc import ILabels
from rmshared.content.taxonomy.core.protocols.abc import IFields
from rmshared.content.taxonomy.core.protocols.abc import IValues


class Labels(ILabels[labels.Label]):
    def __init__(self, fields: IFields, values: IValues):
        self.label_to_delegate_map: Mapping[Type[Label], 'Labels.IDelegate'] = ensure_map_is_complete(labels.Label, {
            labels.Value: self.Value(fields, values),
            labels.Badge: self.Badge(fields),
            labels.Empty: self.Empty(fields),
        })
        self.name_to_delegate_map: Mapping[str, 'Labels.IDelegate'] = dict_from_list(
            source=self.label_to_delegate_map.values(),
            key_func=attrgetter('name'),
        )

    def make_label(self, data):
        name, info = parse_name_and_info(data)
        return self.name_to_delegate_map[name].make_label(info)

    def jsonify_label(self, label):
        delegate = self.label_to_delegate_map[type(label)]
        return {delegate.name: delegate.jsonify_label_info(label)}

    class IDelegate(Generic[Label], metaclass=ABCMeta):
        @property
        @abstractmethod
        def name(self) -> AbstractSet[str]:
            pass

        @abstractmethod
        def make_label(self, info: Mapping[str, Any]) -> Label:
            pass

        @abstractmethod
        def jsonify_label_info(self, label: Label) -> Mapping[str, Any]:
            pass

    class Value(IDelegate[labels.Value]):
        def __init__(self, fields: IFields, values: IValues):
            self.fields = fields
            self.values = values

        @property
        def name(self):
            return 'value'

        def make_label(self, info):
            return labels.Value(
                field=self.fields.make_field(info['field']),
                value=self.values.make_value(info['value']),
            )

        def jsonify_label_info(self, label: labels.Value):
            return {
                'field': self.fields.jsonify_field(label.field),
                'value': self.values.jsonify_value(label.value),
            }

    class Badge(IDelegate[labels.Badge]):
        def __init__(self, fields: IFields):
            self.fields = fields

        @property
        def name(self):
            return 'badge'

        def make_label(self, info):
            return labels.Badge(
                field=self.fields.make_field(info['field']),
            )

        def jsonify_label_info(self, label: labels.Badge):
            return {
                'field': self.fields.jsonify_field(label.field),
            }

    class Empty(IDelegate[labels.Empty]):
        def __init__(self, fields: IFields):
            self.fields = fields

        @property
        def name(self):
            return 'empty'

        def make_label(self, info):
            return labels.Empty(
                field=self.fields.make_field(info['field']),
            )

        def jsonify_label_info(self, label: labels.Empty):
            return {
                'field': self.fields.jsonify_field(label.field),
            }
