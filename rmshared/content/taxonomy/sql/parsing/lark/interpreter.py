from __future__ import annotations

from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Mapping
from collections.abc import Sequence
from typing import Any
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import cast

from lark import Tree
from lark import Token
from lark import visitors

from rmshared.tools import unless_none
from rmshared.typings import read_only

from rmshared import sql

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import tags
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import sections
from rmshared.content.taxonomy import users
from rmshared.content.taxonomy import communities
from rmshared.content.taxonomy import variables
from rmshared.content.taxonomy.abc import Guid

from rmshared.content.taxonomy.sql.parsing import exceptions
from rmshared.content.taxonomy.sql.parsing.lark.contexts import ContextManager

T = TypeVar('T')
F = TypeVar('F')
L = TypeVar('L')
R = TypeVar('R')
V = TypeVar('V')


class Interpreter(visitors.Interpreter, ContextManager):
    GRAMMAR = sql.parsing.lark.read_grammar_lazy('grammar.lark')  # TODO: Decouple from Shared.GRAMMAR

    @sql.parsing.lark.visit_children
    def taxonomy_id_field(self, taxonomy_id_field: Token) -> core.fields.Field:
        alias = cast(str, taxonomy_id_field.value)
        return self.context.fields.resolve_id_field(alias)

    @sql.parsing.lark.visit_children
    def taxonomy_scope(self, scope: Token):
        alias = cast(str, scope.value)
        try:
            entity = self.SCOPE_ALIAS_TO_ENTITY_MAP[alias.lower()]
        except LookupError as e:
            raise exceptions.UnknownScopeError(scope=alias) from e
        else:
            return ContextManager.Scope(alias=alias, entity=entity)

    SCOPE_ALIAS_TO_ENTITY_MAP: Mapping[str, Type[Guid]] = {
        'tags': tags.guids.Tag,
        'posts': posts.guids.Post,
        'users': users.guids.UserProfile,
        'sections': sections.guids.Section,
        'communities': communities.guids.Community,
    }

    @sql.parsing.lark.visit_children
    def taxonomy_filter_return(self, filter_: Tree) -> F:
        filter_ = self.visit(filter_)
        filter_ = self.context.filters.validate_return_filter(filter_)
        return filter_

    @sql.parsing.lark.visit_children
    def taxonomy_filter_switch_if_variable_is_null(self, if_filter: Tree, ref: Tree, otherwise_filter: Tree = None) -> F:
        filter_ = self._visit_filter_switch_if_variable_is_null(ref, if_null_filter=if_filter, if_not_null_filter=otherwise_filter)
        filter_ = self.context.filters.validate_switch_filter(filter_)
        return filter_

    @sql.parsing.lark.visit_children
    def taxonomy_filter_switch_if_variable_is_not_null(self, if_filter: Tree, ref: Tree, otherwise_filter: Tree = None) -> F:
        filter_ = self._visit_filter_switch_if_variable_is_null(ref, if_null_filter=otherwise_filter, if_not_null_filter=if_filter)
        filter_ = self.context.filters.validate_switch_filter(filter_)
        return filter_

    def _visit_filter_switch_if_variable_is_null(self, ref: Tree, if_null_filter: Optional[Tree], if_not_null_filter: Optional[Tree]) -> F:
        ref = cast(variables.Reference, self.visit(ref))
        if_null_filter = unless_none(self.visit, if_none=self.context.filters.make_return_nothing())(if_null_filter)
        if_not_null_filter = unless_none(self.visit, if_none=self.context.filters.make_return_nothing())(if_not_null_filter)
        return variables.operators.Switch(ref=ref, cases=read_only({
            variables.arguments.Any: if_null_filter,
            variables.arguments.Value: if_not_null_filter,
        }))

    @sql.parsing.lark.visit_children
    def taxonomy_filter_is_true(self, field: Tree) -> F:
        field = self.visit(field)
        label = self.context.filters.make_return_badge_label(field)
        return self.context.filters.make_return_any_label_filter(labels=(label,))

    @sql.parsing.lark.visit_children
    def taxonomy_filter_is_false(self, field: Tree) -> F:
        field = self.visit(field)
        label = self.context.filters.make_return_badge_label(field)
        return self.context.filters.make_return_no_labels_filter(labels=(label,))

    @sql.parsing.lark.visit_children
    def taxonomy_filter_is_null(self, field: Tree) -> F:
        field = self.visit(field)
        label = self.context.filters.make_return_empty_label(field)
        return self.context.filters.make_return_any_label_filter(labels=(label,))

    @sql.parsing.lark.visit_children
    def taxonomy_filter_is_not_null(self, field: Tree) -> F:
        field = self.visit(field)
        label = self.context.filters.make_return_empty_label(field)
        return self.context.filters.make_return_no_labels_filter(labels=(label,))

    @sql.parsing.lark.visit_children
    def taxonomy_filter_is_empty(self, field: Tree) -> F:
        field = self.visit(field)
        label = self.context.filters.make_return_empty_label(field)
        return self.context.filters.make_return_any_label_filter(labels=(label,))

    @sql.parsing.lark.visit_children
    def taxonomy_filter_is_not_empty(self, field: Tree) -> F:
        field = self.visit(field)
        label = self.context.filters.make_return_empty_label(field)
        return self.context.filters.make_return_no_labels_filter(labels=(label,))

    @sql.parsing.lark.visit_children
    def taxonomy_filter_is(self, field: Tree, value: Tree) -> F:
        field = self.visit(field)
        value = self.visit(value)
        label = self.context.filters.make_return_value_label(field, value)
        return self.context.filters.make_return_any_label_filter(labels=(label,))

    @sql.parsing.lark.visit_children
    def taxonomy_filter_is_not(self, field: Tree, value: Tree) -> F:
        field = self.visit(field)
        value = self.visit(value)
        label = self.context.filters.make_return_value_label(field, value)
        return self.context.filters.make_return_no_labels_filter(labels=(label,))

    @sql.parsing.lark.visit_children
    def taxonomy_filter_contain(self, field: Tree, value: Tree) -> F:
        field = self.visit(field)
        value = self.visit(value)
        label = self.context.filters.make_return_value_label(field, value)
        return self.context.filters.make_return_any_label_filter(labels=(label,))

    @sql.parsing.lark.visit_children
    def taxonomy_filter_not_contain(self, field: Tree, value: Tree) -> F:
        field = self.visit(field)
        value = self.visit(value)
        label = self.context.filters.make_return_value_label(field, value)
        return self.context.filters.make_return_no_labels_filter(labels=(label,))

    @sql.parsing.lark.visit_children
    def taxonomy_filter_contain_any(self, field: Tree, values: Tree) -> F:
        field = self.visit(field)
        values = self.visit(values)
        labels = self._make_sequence(lambda v: self.context.filters.make_return_value_label(field, v), values)
        return self.context.filters.make_return_any_label_filter(labels)

    @sql.parsing.lark.visit_children
    def taxonomy_filter_contain_none(self, field: Tree, values: Tree) -> F:
        field = self.visit(field)
        values = self.visit(values)
        labels = self._make_sequence(lambda v: self.context.filters.make_return_value_label(field, v), values)
        return self.context.filters.make_return_no_labels_filter(labels)

    @sql.parsing.lark.visit_children
    def taxonomy_filter_in(self, field: Tree, values: Tree) -> F:
        field = self.visit(field)
        values = self.visit(values)
        labels = self._make_sequence(lambda v: self.context.filters.make_return_value_label(field, v), values)
        return self.context.filters.make_return_any_label_filter(labels)

    @sql.parsing.lark.visit_children
    def taxonomy_filter_not_in(self, field: Tree, values: Tree) -> F:
        field = self.visit(field)
        values = self.visit(values)
        labels = self._make_sequence(lambda v: self.context.filters.make_return_value_label(field, v), values)
        return self.context.filters.make_return_no_labels_filter(labels)

    @sql.parsing.lark.visit_children
    def taxonomy_filter_between(self, field: Tree, min_value: Tree, max_value: Tree) -> F:
        field = self.visit(field)
        min_value = self.visit(min_value)
        max_value = self.visit(max_value)
        range_ = self.context.filters.make_return_between_range(field, min_value, max_value)
        return self.context.filters.make_return_any_range_filter(ranges=(range_,))

    @sql.parsing.lark.visit_rules
    def taxonomy_filter_less_than(self, field: Tree, value: Tree) -> F:
        field = self.visit(field)
        value = self.visit(value)
        range_ = self.context.filters.make_return_less_than_range(field, value=value)
        return self.context.filters.make_return_any_range_filter(ranges=(range_,))

    @sql.parsing.lark.visit_rules
    def taxonomy_filter_more_than(self, field: Tree, value: Tree) -> F:
        field = self.visit(field)
        value = self.visit(value)
        range_ = self.context.filters.make_return_more_than_range(field, value=value)
        return self.context.filters.make_return_any_range_filter(ranges=(range_,))

    @classmethod
    def _make_sequence(cls, factory: Callable[[Any], T], values: Iterable[Any]) -> Sequence[T]:
        return tuple(map(factory, values))

    @sql.parsing.lark.visit_children
    def taxonomy_badge_field(self, variant: Tree) -> core.fields.Field:
        return self.visit(variant)

    @sql.parsing.lark.visit_children
    def taxonomy_multi_value_field(self, variant: Tree) -> core.fields.Field:
        return self.visit(variant)

    @sql.parsing.lark.visit_children
    def taxonomy_single_value_field(self, variant: Tree) -> core.fields.Field:
        return self.visit(variant)

    @sql.parsing.lark.visit_children
    def taxonomy_badge_system_field(self, field: Token) -> core.fields.Field:
        return self.context.fields.resolve_badge_system_field(alias=cast(str, field.value))

    @sql.parsing.lark.visit_children
    def taxonomy_multi_value_system_field(self, field: Token) -> core.fields.Field:
        return self.context.fields.resolve_multi_value_system_field(alias=cast(str, field.value))

    @sql.parsing.lark.visit_children
    def taxonomy_single_value_system_field(self, field: Token) -> core.fields.Field:
        return self.context.fields.resolve_single_value_system_field(alias=cast(str, field.value))

    @sql.parsing.lark.visit_children
    def taxonomy_custom_field(self, path: Tree) -> core.fields.Field:
        path = self.visit(path)
        return self.context.fields.resolve_custom_field(path)

    @staticmethod
    @sql.parsing.lark.visit_tokens
    def taxonomy_custom_field_path(path: Token) -> str:
        return cast(str, path.value)

    @sql.parsing.lark.visit_children
    def taxonomy_event(self, event: Token) -> core.events.Event:
        return self.context.fields.resolve_event(alias=cast(str, event.value))

    @sql.parsing.lark.visit_children
    def taxonomy_constant(self, taxonomy_scalar: Tree) -> V:
        scalar = self.visit(taxonomy_scalar)
        return self.context.filters.make_constant_value(scalar)

    @sql.parsing.lark.visit_children
    def taxonomy_variable(self, ref: Tree, index: Tree = None) -> V:
        ref = self.visit(ref)
        index = unless_none(self.visit, if_none=0)(index)
        return self.context.filters.make_variable_value(ref, index)

    @sql.parsing.lark.visit_children
    def taxonomy_variable_reference_by_index(self, index: Token) -> variables.Reference:
        index = int(cast(str, index.value)[2:])
        return self.context.filters.resolve_reference_by_index(index)

    @sql.parsing.lark.visit_children
    def taxonomy_variable_reference_by_alias(self, alias: Token) -> variables.Reference:
        alias = cast(str, alias.value)[1:]
        return self.context.filters.resolve_reference_by_alias(alias)
