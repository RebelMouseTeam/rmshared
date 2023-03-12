from typing import Mapping
from typing import NoReturn
from typing import Type
from typing import TypeVar
from typing import get_origin

from rmshared.content.taxonomy.visitors.abc import IRanges

InRange = TypeVar('InRange')
OutRange = TypeVar('OutRange')


class Ranges(IRanges[InRange, OutRange]):
    def __init__(self, range_to_visitor_map: Mapping[Type[InRange], IRanges[InRange, OutRange]] = None):
        self.range_to_visitor_map = dict(range_to_visitor_map or dict())

    def add_range(self, range_type: Type[InRange], visitor: IRanges[InRange, OutRange]) -> NoReturn:
        self.range_to_visitor_map[get_origin(range_type) or range_type] = visitor

    def visit_range(self, range_: InRange) -> OutRange:
        return self.range_to_visitor_map[type(range_)].visit_range(range_)
