from __future__ import annotations

from collections.abc import Collection
from collections.abc import Mapping
from functools import cached_property
from operator import attrgetter
from typing import Any
from typing import Type
from typing import TypeVar

from rmshared.tools import dict_from_list
from rmshared.tools import group_to_mapping
from rmshared.typings import read_only

from rmshared.content.taxonomy.sql.descriptors import scopes
from rmshared.content.taxonomy.sql.descriptors import exceptions
from rmshared.content.taxonomy.sql.descriptors.abc import IRegistry
from rmshared.content.taxonomy.sql.descriptors.beans import Descriptor

T = TypeVar('T', bound=Any)


class Registry(IRegistry):
    def __init__(self, descriptors: Collection[Descriptor]):
        self.descriptors = descriptors

    def get_descriptor(self, subject):
        try:
            return self.subject_to_descriptor_map[subject]
        except LookupError as e:
            raise exceptions.SubjectNotFoundException(subject) from e

    @cached_property
    def subject_to_descriptor_map(self) -> Mapping[T, Descriptor[T]]:
        return read_only(dict_from_list(self.descriptors, key_func=attrgetter('subject')))

    def find_descriptor(self, alias, scope, subject_type):
        try:
            return self.alias_and_scope_and_subject_type_to_descriptor_map[alias, scope, subject_type]
        except LookupError as e:
            raise exceptions.DescriptorNotFoundException(alias, scope, subject_type) from e

    @cached_property
    def alias_and_scope_and_subject_type_to_descriptor_map(self) -> Mapping[tuple[str, scopes.Scope, Type[T]], Descriptor[T]]:
        def _stream_items():
            for descriptor in self.descriptors:
                for alias in descriptor.aliases:
                    yield (alias, descriptor.scope, type(descriptor.subject)), descriptor

        return read_only(dict(_stream_items()))

    def find_all(self, subject_type):
        return self.subject_type_to_descriptors_map.get(subject_type, tuple())

    @cached_property
    def subject_type_to_descriptors_map(self) -> Mapping[Type[T], Collection[Descriptor[T]]]:
        return read_only(group_to_mapping(self.descriptors, key_func=lambda descriptor: type(descriptor.subject)))
