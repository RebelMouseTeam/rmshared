from typing import Mapping
from typing import NoReturn
from typing import Type
from typing import TypeVar
from typing import get_origin

from rmshared.content.taxonomy.visitors.abc import ILabels

InLabel = TypeVar('InLabel')
OutLabel = TypeVar('OutLabel')


class Labels(ILabels[InLabel, OutLabel]):
    def __init__(self, label_to_visitor_map: Mapping[Type[InLabel], ILabels[InLabel, OutLabel]] = None):
        self.label_to_visitor_map = dict(label_to_visitor_map or dict())

    def add_label(self, label_type: Type[InLabel], visitor: ILabels) -> NoReturn:
        self.label_to_visitor_map[get_origin(label_type) or label_type] = visitor

    def visit_label(self, label: InLabel) -> OutLabel:
        return self.label_to_visitor_map[type(label)].visit_label(label)
