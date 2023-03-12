from typing import Mapping
from typing import NoReturn
from typing import Type
from typing import TypeVar
from typing import get_origin

from rmshared.content.taxonomy.visitors.abc import IValues

InValue = TypeVar('InValue')
OutValue = TypeVar('OutValue')


class Values(IValues[InValue, OutValue]):
    def __init__(self, value_to_visitor_map: Mapping[Type[InValue], IValues[InValue, OutValue]] = None):
        self.value_to_visitor_map = dict(value_to_visitor_map or dict())

    def add_value(self, value_type: Type[InValue], visitor: IValues) -> NoReturn:
        self.value_to_visitor_map[get_origin(value_type) or value_type] = visitor

    def visit_value(self, value: InValue) -> OutValue:
        return self.value_to_visitor_map[type(value)].visit_value(value)
