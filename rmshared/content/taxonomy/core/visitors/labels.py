from dataclasses import replace
from typing import Iterator
from typing import TypeVar

from rmshared.content.taxonomy import visitors
from rmshared.content.taxonomy.core import labels

Field = TypeVar('Field')
InValue = TypeVar('InValue')
OutValue = TypeVar('OutValue')


class ExpandValue(visitors.ILabels[labels.Value, Iterator[labels.Value]]):
    def __init__(self, values: visitors.IValues[InValue, OutValue]):
        self.values = values

    def visit_label(self, label: labels.Value[Field, InValue]) -> Iterator[labels.Value[Field, OutValue]]:
        yield replace(label, value=self.values.visit_value(label.value))


class ExpandAsIs(visitors.ILabels[labels.Label, Iterator[labels.Label]]):
    def visit_label(self, label):
        yield label
