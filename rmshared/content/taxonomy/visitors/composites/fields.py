from typing import Mapping
from typing import NoReturn
from typing import Type
from typing import TypeVar
from typing import get_origin

from rmshared.content.taxonomy.visitors.abc import IFields

InField = TypeVar('InField')
OutField = TypeVar('OutField')


class Fields(IFields[InField, OutField]):
    def __init__(self, field_to_visitor_map: Mapping[Type[InField], IFields[InField, OutField]] = None):
        self.field_to_visitor_map = dict(field_to_visitor_map or dict())

    def add_field(self, field_type: Type[InField], visitor: IFields) -> NoReturn:
        self.field_to_visitor_map[get_origin(field_type) or field_type] = visitor

    def visit_field(self, field: InField) -> OutField:
        return self.field_to_visitor_map[type(field)].visit_field(field)
