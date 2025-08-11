from __future__ import annotations

from collections.abc import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.sql import compiling

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core.sql.compiling.abc import IDescriptors
from rmshared.content.taxonomy.core.sql.compiling.abc import IFields

F = TypeVar('F', bound=fields.Field)


class Fields(IFields[fields.Field]):
    def __init__(self, descriptors: IDescriptors):
        self.descriptors = descriptors
        self.field_to_make_tree_func_map: Mapping[Type[F], compiling.MakeTreeFunc[F]] = ensure_map_is_complete(fields.Field, {
            fields.System: self._make_tree_from_system_field,
            fields.Custom: self._make_tree_from_custom_field,
        })

    def make_field_operations(self, field):
        if self._is_custom_field(field):
            return self._make_custom_field_operations(field)
        elif self.descriptors.is_badge_field(field):
            return self._make_boolean_field_operations(field)
        if self.descriptors.is_multi_value_field(field):
            return self._make_multi_value_field_match_operations(field)
        elif self.descriptors.is_single_value_field(field):
            return self._make_single_value_field_match_operations(field)
        else:
            raise ValueError(f'Unsupported field: {field!r}. Expected a custom, boolean, single-value, or multi-value field.')

    @staticmethod
    def _is_custom_field(field: fields.Field) -> bool:
        return isinstance(field, fields.Custom)

    def _make_custom_field_operations(self, field: fields.Custom) -> IFields.IOperations:
        field = self._make_tree_from_custom_field(field)
        return self.CustomFieldOperations(field)

    def _make_boolean_field_operations(self, field: fields.System) -> IFields.IOperations:
        field = self._make_tree_from_system_field(field)
        return self.BadgeFieldOperations(field)

    def _make_single_value_field_match_operations(self, field: fields.System) -> IFields.IOperations:
        field = self._make_tree_from_system_field(field)
        return self.SingleValueFieldMatchOperations(field)

    def _make_multi_value_field_match_operations(self, field: fields.System) -> IFields.IOperations:
        field = self._make_tree_from_system_field(field)
        return self.MultiValueFieldOperations(field)

    def make_tree_from_field(self, field: fields.Field):
        return self.field_to_make_tree_func_map[type(field)](field)

    def _make_tree_from_system_field(self, field: fields.System) -> compiling.ITree:
        alias = self.descriptors.get_field_alias(field)
        return compiling.terminals.CName(alias)

    @staticmethod
    def _make_tree_from_custom_field(field: fields.Custom) -> compiling.ITree:
        name = compiling.terminals.CName('CUSTOM_FIELD')
        args = compiling.terminals.String(field.path)
        tree = compiling.functions.Function(name, args)
        return compiling.utils.Joined(tree, separator='')

    class CustomFieldOperations(IFields.IOperations):
        def __init__(self, field: compiling.ITree):
            self.boolean_operations = Fields.BadgeFieldOperations(field)
            self.multi_value_operations = Fields.MultiValueFieldOperations(field)
            self.single_value_operations = Fields.SingleValueFieldMatchOperations(field)

        def make_match_badge_operation(self):
            return self.boolean_operations.make_match_badge_operation()

        def make_does_not_match_badge_operation(self):
            return self.boolean_operations.make_does_not_match_badge_operation()

        def make_match_empty_operation(self):
            return self.multi_value_operations.make_match_empty_operation()

        def make_does_not_match_empty_operation(self):
            return self.multi_value_operations.make_does_not_match_empty_operation()

        def make_match_one_value_operation(self, expression):
            return self.multi_value_operations.make_match_one_value_operation(expression)

        def make_does_not_match_one_value_operation(self, expression):
            return self.multi_value_operations.make_does_not_match_one_value_operation(expression)

        def make_match_any_value_operation(self, expression):
            return self.multi_value_operations.make_match_any_value_operation(expression)

        def make_does_not_match_any_value_operation(self, expression):
            return self.multi_value_operations.make_does_not_match_any_value_operation(expression)

        def make_between_operation(self, min_value, max_value):
            return self.single_value_operations.make_between_operation(min_value, max_value)

        def make_not_between_operation(self, min_value, max_value):
            return self.single_value_operations.make_not_between_operation(min_value, max_value)

        def make_less_than_operation(self, value):
            return self.single_value_operations.make_less_than_operation(value)

        def make_less_than_or_equal_operation(self, value):
            return self.single_value_operations.make_less_than_or_equal_operation(value)

        def make_more_than_operation(self, value):
            return self.single_value_operations.make_more_than_operation(value)

        def make_more_than_or_equal_operation(self, value):
            return self.single_value_operations.make_more_than_or_equal_operation(value)

    class UnsupportedOperations(IFields.IOperations):
        TYPE: str

        def __init__(self, field: compiling.ITree):
            self.field = field

        def make_match_badge_operation(self):
            raise ValueError(f'Boolean operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

        def make_does_not_match_badge_operation(self):
            raise ValueError(f'Boolean operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

        def make_match_empty_operation(self):
            raise ValueError(f'Empty match operation is not supported for {self.TYPE} fields. Field: {self.field!r}')

        def make_does_not_match_empty_operation(self):
            raise ValueError(f'Empty match operation is not supported for {self.TYPE} fields. Field: {self.field!r}')

        def make_match_one_value_operation(self, expression):
            raise ValueError(f'Comparison operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

        def make_does_not_match_one_value_operation(self, expression):
            raise ValueError(f'Comparison operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

        def make_match_any_value_operation(self, expression):
            raise ValueError(f'Comparison operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

        def make_does_not_match_any_value_operation(self, expression):
            raise ValueError(f'Comparison operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

        def make_between_operation(self, min_value, max_value):
            raise ValueError(f'Comparison operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

        def make_not_between_operation(self, min_value, max_value):
            raise ValueError(f'Comparison operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

        def make_less_than_operation(self, value):
            raise ValueError(f'Comparison operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

        def make_less_than_or_equal_operation(self, value):
            raise ValueError(f'Comparison operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

        def make_more_than_operation(self, value):
            raise ValueError(f'Comparison operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

        def make_more_than_or_equal_operation(self, value):
            raise ValueError(f'Comparison operations are not supported for {self.TYPE} fields: Field: {self.field!r}')

    class BadgeFieldOperations(UnsupportedOperations):
        TYPE = 'boolean'

        def make_match_badge_operation(self):
            return self.field

        def make_does_not_match_badge_operation(self):
            return compiling.logical.Negation(self.field)

    class SingleValueFieldMatchOperations(UnsupportedOperations):
        TYPE = 'single-value'

        def make_match_empty_operation(self):
            return compiling.operations.IsNull(self.field)

        def make_does_not_match_empty_operation(self):
            return compiling.operations.IsNotNull(self.field)

        def make_match_one_value_operation(self, expression):
            return compiling.operations.IsEqual(self.field, expression)

        def make_does_not_match_one_value_operation(self, expression):
            return compiling.operations.IsNotEqual(self.field, expression)

        def make_match_any_value_operation(self, expression):
            return compiling.operations.IsIn(self.field, expression)

        def make_does_not_match_any_value_operation(self, expression):
            return compiling.operations.IsNotIn(self.field, expression)

        def make_between_operation(self, min_value, max_value):
            return compiling.operations.Between(self.field, min_value, max_value)

        def make_not_between_operation(self, min_value, max_value):
            expression = self.make_between_operation(min_value, max_value)
            return compiling.logical.Negation(expression)

        def make_less_than_operation(self, value):
            return compiling.operations.IsLessThan(self.field, value)

        def make_less_than_or_equal_operation(self, value):
            return compiling.operations.IsLessThanOrEqual(self.field, value)

        def make_more_than_operation(self, value):
            return compiling.operations.IsMoreThan(self.field, value)

        def make_more_than_or_equal_operation(self, value):
            return compiling.operations.IsMoreThanOrEqual(self.field, value)

    class MultiValueFieldOperations(UnsupportedOperations):
        TYPE = 'multi-value'

        def make_match_empty_operation(self):
            return compiling.operations.IsEmpty(self.field)

        def make_does_not_match_empty_operation(self):
            return compiling.operations.IsNotEmpty(self.field)

        def make_match_one_value_operation(self, expression):
            return compiling.operations.Contain(self.field, expression)

        def make_does_not_match_one_value_operation(self, expression):
            return compiling.operations.NotContain(self.field, expression)

        def make_match_any_value_operation(self, expression):
            return compiling.operations.ContainAny(self.field, expression)

        def make_does_not_match_any_value_operation(self, expression):
            return compiling.operations.ContainNone(self.field, expression)
