from typing import TypeVar

from rmshared.content.taxonomy import visitors

Field = TypeVar('Field')


class AsIs(visitors.IFields[Field, Field]):
    def visit_field(self, field):
        return field
