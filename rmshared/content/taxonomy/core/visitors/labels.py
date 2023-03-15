from typing import Iterator
from typing import TypeVar

from rmshared.content.taxonomy import visitors
from rmshared.content.taxonomy.core import labels

InField = TypeVar('InField')
OutField = TypeVar('OutField')
InValue = TypeVar('InValue')
OutValue = TypeVar('OutValue')


class ExpandValue(visitors.ILabels[labels.Value, Iterator[labels.Value]]):
    def __init__(self, fields: visitors.IFields[InField, OutField], values: visitors.IValues[InValue, OutValue]):
        self.fields = fields
        self.values = values

    def visit_label(self, label: labels.Value[InField, InValue]) -> Iterator[labels.Value[OutField, OutValue]]:
        field = self.fields.visit_field(label.field)
        value = self.values.visit_value(label.value)
        yield labels.Value(field, value)


class ExpandBadge(visitors.ILabels[labels.Badge, Iterator[labels.Badge]]):
    def __init__(self, fields: visitors.IFields[InField, OutField]):
        self.fields = fields

    def visit_label(self, label: labels.Badge[InField]) -> Iterator[labels.Badge[OutField]]:
        field = self.fields.visit_field(label.field)
        yield labels.Badge(field)


class ExpandEmpty(visitors.ILabels[labels.Empty, Iterator[labels.Empty]]):
    def __init__(self, fields: visitors.IFields[InField, OutField]):
        self.fields = fields

    def visit_label(self, label: labels.Empty[InField]) -> Iterator[labels.Empty[OutField]]:
        field = self.fields.visit_field(label.field)
        yield labels.Empty(field)
