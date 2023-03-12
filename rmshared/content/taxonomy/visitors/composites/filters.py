from typing import Mapping
from typing import NoReturn
from typing import Type
from typing import TypeVar
from typing import get_origin

from rmshared.content.taxonomy.visitors.abc import IFilters

InFilter = TypeVar('InFilter')
OutFilter = TypeVar('OutFilter')


class Filters(IFilters[InFilter, OutFilter]):
    def __init__(self, filter_to_visitor_map: Mapping[Type[InFilter], IFilters[InFilter, OutFilter]] = None):
        self.filter_to_visitor_map = dict(filter_to_visitor_map or dict())

    def add_filter(self, filter_type: Type[InFilter], visitor: IFilters[InFilter, OutFilter]) -> NoReturn:
        self.filter_to_visitor_map[get_origin(filter_type) or filter_type] = visitor

    def visit_filter(self, filter_: InFilter) -> OutFilter:
        return self.filter_to_visitor_map[type(filter_)].visit_filter(filter_)
