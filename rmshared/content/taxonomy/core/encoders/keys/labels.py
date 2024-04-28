from typing import Callable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core.encoders.abc import IFields
from rmshared.content.taxonomy.core.encoders.abc import ILabels
from rmshared.content.taxonomy.core.encoders.abc import IValues

Label = TypeVar('Label', bound=labels.Label)


class Labels(ILabels[labels.Label, str]):
    def __init__(self, fields: IFields, values: IValues):
        self.fields = fields
        self.values = values
        self.label_to_delegate_map: Mapping[Type[Label], Callable[[Label], str]] = ensure_map_is_complete(labels.Label, {
            labels.Value: self._encode_value_label,
            labels.Badge: self._encode_badge_label,
            labels.Empty: self._encode_empty_label,
        })

    def encode_label(self, label):
        return self.label_to_delegate_map[type(label)](label)

    def _encode_value_label(self, label: labels.Value):
        field = self.fields.encode_field(label.field)
        value = self.values.encode_value(label.value)
        return f'{field}={value}'

    def _encode_badge_label(self, label: labels.Badge):
        field = self.fields.encode_field(label.field)
        return f'{field}+'

    def _encode_empty_label(self, label: labels.Empty):
        field = self.fields.encode_field(label.field)
        return f'{field}-'
