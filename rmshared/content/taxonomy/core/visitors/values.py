from typing import TypeVar

from rmshared.content.taxonomy import visitors

Value = TypeVar('Value')


class AsIs(visitors.IValues[Value, Value]):
    def visit_value(self, value):
        return value
