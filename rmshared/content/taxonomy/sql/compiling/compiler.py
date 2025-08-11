from __future__ import annotations

from collections.abc import Iterator
from collections.abc import Mapping
from functools import cached_property
from typing import Type
from typing import TypeVar

from rmshared.typings import read_only

from rmshared.tools import ensure_map_is_likely_complete

from rmshared.sql import compiling

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import variables
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import users
from rmshared.content.taxonomy import tags
from rmshared.content.taxonomy import sections
from rmshared.content.taxonomy import communities
from rmshared.content.taxonomy.abc import Guid

from rmshared.content.taxonomy.sql import descriptors

F = TypeVar('F', bound=core.fields.Field)
L = TypeVar('L', bound=core.labels.Label)
E = TypeVar('E', bound=core.events.Event)
O = TypeVar('O', bound=variables.Operator)
A = TypeVar('A', bound=variables.Argument)
S = TypeVar('S')


class Compiler:
    def __init__(self):
        self.descriptors = self.Descriptors(registry=descriptors.Factory.make_registry())
        self.core = core.sql.compiling.Factory.make_instance(self.descriptors).make_composite()
        self.variables = variables.sql.compiling.Factory.make_instance(self.descriptors).make_composite()
        self.guid_to_scope_map = ensure_map_is_likely_complete(Guid, {
            tags.guids.Tag: 'tags',
            posts.guids.Post: 'posts',
            sections.guids.Section: 'sections',
            users.guids.UserProfile: 'users',
            communities.guids.Community: 'communities',
        })

    def make_tree_from_scope(self, entity: Type[Guid]) -> compiling.ITree:
        scope = self.guid_to_scope_map[entity]
        return compiling.terminals.CName(scope)

    def make_tree_from_id_field(self, entity: Type[Guid]) -> compiling.ITree:
        alias = self.descriptors.get_id_field_alias(entity)
        return compiling.terminals.CName(alias)

    def make_tree_from_constant_filter(self, filter_: core.filters.Filter) -> compiling.ITree:
        tree = self.core.make_tree_from_filter(filter_)
        tree = compiling.utils.Compacted(tree, compiling.compact.with_space)
        return tree

    def make_tree_from_variable_filter(self, filter_: variables.Operator[core.filters.Filter]) -> compiling.ITree:
        tree = self.variables.make_tree_from_filter(filter_)
        tree = compiling.utils.Compacted(tree, compiling.compact.with_space)
        return tree

    def make_tree_from_variable_reference(self, reference: variables.Reference) -> compiling.ITree:
        tree = self.variables.make_tree_from_reference(reference)
        tree = compiling.utils.Compacted(tree, compiling.compact.with_nothing)
        return tree

    def make_tree_from_field(self, field: core.fields.Field) -> compiling.ITree:
        return self.core.make_tree_from_field(field)

    def make_tree_from_event(self, event: core.events.Event) -> compiling.ITree:
        return self.core.make_tree_from_event(event)

    def make_tree_from_scalar(self, scalar: str | int | float) -> compiling.ITree:
        return self.core.make_tree_from_value(scalar)

    class Descriptors(core.sql.compiling.IDescriptors[core.fields.System, core.events.Event]):
        def __init__(self, registry: descriptors.IRegistry):
            self.registry = registry

        def is_badge_field(self, field):
            descriptor = self.registry.get_descriptor(subject=field)
            return descriptors.options.Badge() in descriptor.options

        def is_multi_value_field(self, field):
            descriptor = self.registry.get_descriptor(subject=field)
            return descriptors.options.MultiValue() in descriptor.options

        def is_single_value_field(self, field):
            descriptor = self.registry.get_descriptor(subject=field)
            return descriptors.options.SingleValue() in descriptor.options

        def get_field_alias(self, field):
            descriptor = self.registry.get_descriptor(subject=field)
            return descriptor.aliases[0]

        def get_event_alias(self, event):
            descriptor = self.registry.get_descriptor(subject=event)
            return descriptor.aliases[0]

        def get_id_field_alias(self, entity):
            return self.id_field_aliases_map[entity]

        @cached_property
        def id_field_aliases_map(self) -> Mapping[Type[Guid], str]:
            def _stream_items() -> Iterator[tuple[Type[Guid], str]]:
                for descriptor in self.registry.find_all(subject_type=core.fields.System):
                    if descriptors.options.Id() not in descriptor.options:
                        continue
                    if isinstance(descriptor.scope, descriptors.scopes.Entity):
                        yield descriptor.scope.entity, descriptor.aliases[0]

            return read_only(dict(_stream_items()))
