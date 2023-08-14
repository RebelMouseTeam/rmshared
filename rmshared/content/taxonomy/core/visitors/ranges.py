from dataclasses import replace
from typing import Iterator
from typing import TypeVar

from rmshared.content.taxonomy import visitors
from rmshared.content.taxonomy.core import ranges

Field = TypeVar('Field')
InValue = TypeVar('InValue')
OutValue = TypeVar('OutValue')


class ExpandBetween(visitors.IRanges[ranges.Between[Field, InValue], Iterator[ranges.Between[Field, OutValue]]]):
    def __init__(self, values: visitors.IValues[InValue, OutValue]):
        self.values = values

    def visit_range(self, range_: ranges.Between[Field, InValue]) -> Iterator[ranges.Between[Field, OutValue]]:
        min_value = self.values.visit_value(range_.min_value)
        max_value = self.values.visit_value(range_.max_value)
        yield replace(range_, min_value=min_value, max_value=max_value)


class ExpandLessThan(visitors.IRanges[ranges.LessThan[Field, InValue], Iterator[ranges.LessThan[Field, OutValue]]]):
    def __init__(self, values: visitors.IValues[InValue, OutValue]):
        self.values = values

    def visit_range(self, range_: ranges.LessThan[Field, InValue]) -> Iterator[ranges.LessThan[Field, OutValue]]:
        yield replace(range_, value=self.values.visit_value(range_.value))


class ExpandMoreThan(visitors.IRanges[ranges.MoreThan[Field, InValue], Iterator[ranges.MoreThan[Field, OutValue]]]):
    def __init__(self, values: visitors.IValues[InValue, OutValue]):
        self.values = values

    def visit_range(self, range_: ranges.MoreThan[Field, InValue]) -> Iterator[ranges.MoreThan[Field, OutValue]]:
        yield replace(range_, value=self.values.visit_value(range_.value))
