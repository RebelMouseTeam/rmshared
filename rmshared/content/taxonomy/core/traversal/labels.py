from collections.abc import Callable
from collections.abc import Mapping
from typing import Any
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core.traversal import visitors
from rmshared.content.taxonomy.core.traversal.abc import ILabels

Label = TypeVar('Label', bound=labels.Label)


class Labels(ILabels[Label]):
    def __init__(self):
        self.label_to_traverse_func_map: Mapping[Type[Label], Callable[[Label, Any], None]] = ensure_map_is_complete(labels.Label, {
            labels.Value: self._traverse_value_label,
            labels.Badge: self._traverse_badge_label,
            labels.Empty: self._traverse_empty_label,
        })

    def traverse_labels(self, labels_, visitor) -> None:
        for label_ in labels_:
            self._enter_label(label_, visitor=visitors.Labels(delegate=visitor))
            self._traverse_label(label_, visitor)
            self._leave_label(label_, visitor=visitors.Labels(delegate=visitor))

    @staticmethod
    def _enter_label(label_: Label, visitor: visitors.ILabels) -> None:
        return visitor.enter_label(label_)

    @staticmethod
    def _leave_label(label_: Label, visitor: visitors.ILabels) -> None:
        return visitor.leave_label(label_)

    def _traverse_label(self, label_: Label, visitor: Any) -> None:
        self.label_to_traverse_func_map[type(label_)](label_, visitor)

    def _traverse_value_label(self, label_: labels.Value, visitor: Any) -> None:
        self._visit_field(label_.field, visitor=visitors.Fields(delegate=visitor))
        self._visit_value(label_.value, visitor=visitors.Values(delegate=visitor))

    def _traverse_badge_label(self, label_: labels.Badge, visitor: Any) -> None:
        self._visit_field(label_.field, visitor=visitors.Fields(delegate=visitor))

    def _traverse_empty_label(self, label_: labels.Empty, visitor: Any) -> None:
        self._visit_field(label_.field, visitor=visitors.Fields(delegate=visitor))

    @staticmethod
    def _visit_field(field, visitor: visitors.IFields) -> None:
        return visitor.visit_field(field)

    @staticmethod
    def _visit_value(value, visitor: visitors.IValues) -> None:
        return visitor.visit_value(value)
