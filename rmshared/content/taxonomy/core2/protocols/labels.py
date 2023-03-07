from typing import Any
from typing import Callable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import invert_dict
from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.core2 import labels
from rmshared.content.taxonomy.core2.protocols.abc import ILabels
from rmshared.content.taxonomy.core2.protocols.abc import IFields
from rmshared.content.taxonomy.core2.protocols.abc import IValues


class Labels(ILabels[labels.Label]):
    L = TypeVar('L', bound=labels.Label)

    def __init__(self, fields: IFields, values: IValues):
        self.fields = fields
        self.values = values
        self.label_to_label_name_map: Mapping[Type[labels.Label], str] = {
            labels.Value: 'value',
            labels.Badge: 'badge',
            labels.Empty: 'empty',
        }
        self.label_name_to_label_map: Mapping[str, Type[labels.Label]] = invert_dict(self.label_to_label_name_map)
        self.label_to_factory_func_map: Mapping[Type[labels.Label], Callable[[Mapping[str, Any]], labels.Label]] = {
            labels.Value: self._make_value_label,
            labels.Badge: self._make_badge_label,
            labels.Empty: self._make_empty_label,
        }
        self.label_to_jsonify_func_map: Mapping[Type[labels.Label], Callable[[Labels.L], Mapping[str, Any]]] = {
            labels.Value: self._jsonify_value_label_info,
            labels.Badge: self._jsonify_badge_label_info,
            labels.Empty: self._jsonify_empty_label_info,
        }

    def make_label(self, data):
        name, info = parse_name_and_info(data)
        label_type = self.label_name_to_label_map[name]
        return self.label_to_factory_func_map[label_type](info)

    def jsonify_label(self, label):
        name = self.label_to_label_name_map[type(label)]
        info = self.label_to_jsonify_func_map[type(label)](label)
        return {name: info}

    def _make_value_label(self, info: Mapping[str, Any]):
        return labels.Value(
            field=self.fields.make_field(info['field']),
            value=self.values.make_value(info['value']),
        )

    def _jsonify_value_label_info(self, label: labels.Value) -> Mapping[str, Any]:
        return {
            'field': self.fields.jsonify_field(label.field),
            'value': self.values.jsonify_value(label.value),
        }

    def _make_badge_label(self, info: Mapping[str, Any]):
        return labels.Badge(field=self.fields.make_field(info['field']))

    def _jsonify_badge_label_info(self, label: labels.Badge) -> Mapping[str, Any]:
        return {
            'field': self.fields.jsonify_field(label.field),
        }

    def _make_empty_label(self, info: Mapping[str, Any]):
        return labels.Empty(field=self.fields.make_field(info['field']))

    def _jsonify_empty_label_info(self, label: labels.Empty) -> Mapping[str, Any]:
        return {
            'field': self.fields.jsonify_field(label.field),
        }
