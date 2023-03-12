from typing import Iterator
from typing import TypeVar

from rmshared.content.taxonomy import visitors
from rmshared.content.taxonomy.core2 import ranges

InField = TypeVar('InField')
OutField = TypeVar('OutField')
InValue = TypeVar('InValue')
OutValue = TypeVar('OutValue')


class ExpandBetween(visitors.IRanges[ranges.Between[InField, InValue], Iterator[ranges.Between[OutField, OutValue]]]):
    def __init__(self, fields: visitors.IFields[InField, OutField], values: visitors.IValues[InValue, OutValue]):
        self.fields = fields
        self.values = values

    def visit_range(self, range_: ranges.Between[InField, InValue]) -> Iterator[ranges.Between[OutField, OutValue]]:
        field = self.fields.visit_field(range_.field)
        min_value = self.values.visit_value(range_.min_value)
        max_value = self.values.visit_value(range_.max_value)
        yield ranges.Between(field, min_value, max_value)


class ExpandLessThan(visitors.IRanges[ranges.LessThan[InField, InValue], Iterator[ranges.LessThan[OutField, OutValue]]]):
    def __init__(self, fields: visitors.IFields[InField, OutField], values: visitors.IValues[InValue, OutValue]):
        self.fields = fields
        self.values = values

    def visit_range(self, range_: ranges.LessThan[InField, InValue]) -> Iterator[ranges.LessThan[OutField, OutValue]]:
        field = self.fields.visit_field(range_.field)
        value = self.values.visit_value(range_.value)
        yield ranges.LessThan(field, value)


class ExpandMoreThan(visitors.IRanges[ranges.MoreThan[InField, InValue], Iterator[ranges.MoreThan[OutField, OutValue]]]):
    def __init__(self, fields: visitors.IFields[InField, OutField], values: visitors.IValues[InValue, OutValue]):
        self.fields = fields
        self.values = values

    def visit_range(self, range_: ranges.MoreThan[InField, InValue]) -> Iterator[ranges.MoreThan[OutField, OutValue]]:
        field = self.fields.visit_field(range_.field)
        value = self.values.visit_value(range_.value)
        yield ranges.MoreThan(field, value)
