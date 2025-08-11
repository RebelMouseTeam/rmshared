from __future__ import annotations

import warnings

from collections.abc import Callable
from collections.abc import Mapping
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import posts
from rmshared.content.taxonomy import sections
from rmshared.content.taxonomy import users
from rmshared.content.taxonomy.abc import Guid

from rmshared.content.taxonomy.sql import descriptors
from rmshared.content.taxonomy.sql.parsing import exceptions
from rmshared.content.taxonomy.sql.parsing.lark.abc import IContextManager
from rmshared.content.taxonomy.sql.parsing.lark.abc import IFields

Subject = TypeVar('Subject')


class Fields(IFields):
    @classmethod
    def make_instance(cls, scope: IContextManager.Scope) -> Fields:
        return cls(scope, descriptors_=descriptors.Factory().make_registry())

    def __init__(self, scope: IContextManager.Scope, descriptors_: descriptors.IRegistry):
        self.scope = scope
        self.descriptors = descriptors_
        self.entity_to_custom_field_factory_map: Mapping[Type[Guid], Callable[[str], core.fields.Field]] = {
            posts.guids.Post: posts.fields.CustomField,
            users.guids.UserProfile: users.fields.CustomField,
            sections.guids.Section: sections.fields.CustomField,
        }

    def resolve_id_field(self, alias):
        descriptor = self._lookup_field_descriptor(alias)
        descriptor = self._ensure_field_is_id(descriptor, alias)
        return descriptor.subject

    def resolve_badge_system_field(self, alias):
        descriptor = self._lookup_field_descriptor(alias)
        descriptor = self._ensure_field_is_badge(descriptor, alias)
        return descriptor.subject

    def resolve_multi_value_system_field(self, alias):
        descriptor = self._lookup_field_descriptor(alias)
        descriptor = self._ensure_field_is_multi_value(descriptor, alias)
        return descriptor.subject

    def resolve_single_value_system_field(self, alias):
        descriptor = self._lookup_field_descriptor(alias)
        descriptor = self._ensure_field_is_single_value(descriptor, alias)
        return descriptor.subject

    def _lookup_field_descriptor(self, alias: str) -> descriptors.Descriptor[core.fields.System]:
        scope = descriptors.scopes.Entity(self.scope.entity)
        try:
            return self.descriptors.find_descriptor(alias, scope, subject_type=core.fields.System)
        except descriptors.exceptions.DescriptorNotFoundException as e:
            raise exceptions.UnknownFieldError(scope=self.scope.alias, field=alias) from e

    def resolve_custom_field(self, path):
        try:
            return self.entity_to_custom_field_factory_map[self.scope.entity](path)
        except LookupError as e:
            raise exceptions.CustomFieldScopeError(scope=self.scope.alias) from e

    def resolve_event(self, alias):
        descriptor = self._lookup_event_descriptor(alias)
        descriptor = self._ensure_event_is_available(descriptor, alias)
        return descriptor.subject

    def _lookup_event_descriptor(self, alias: str) -> descriptors.Descriptor[core.events.Event]:
        scope = descriptors.scopes.Entity(self.scope.entity)
        try:
            return self.descriptors.find_descriptor(alias, scope, subject_type=core.events.Event)
        except descriptors.exceptions.DescriptorNotFoundException as e:
            raise exceptions.UnknownEventError(scope=self.scope.alias, event=alias) from e

    def _ensure_field_is_id(self, descriptor: descriptors.Descriptor[Subject], alias: str) -> descriptors.Descriptor[Subject]:
        if descriptors.options.Id() not in descriptor.options:
            raise exceptions.NotIdFieldError(scope=self.scope.alias, field=alias)

        return descriptor

    def _ensure_field_is_badge(self, descriptor: descriptors.Descriptor[Subject], alias: str) -> descriptors.Descriptor[Subject]:
        if descriptors.options.Badge() not in descriptor.options:
            raise exceptions.NotBadgeFieldError(scope=self.scope.alias, field=alias)

        return descriptor

    def _ensure_field_is_multi_value(self, descriptor: descriptors.Descriptor[Subject], alias: str) -> descriptors.Descriptor[Subject]:
        if descriptors.options.MultiValue() not in descriptor.options:
            raise exceptions.NotMultiValueFieldError(scope=self.scope.alias, field=alias)

        return descriptor

    def _ensure_field_is_single_value(self, descriptor: descriptors.Descriptor[Subject], alias: str) -> descriptors.Descriptor[Subject]:
        if descriptors.options.SingleValue() not in descriptor.options:
            raise exceptions.NotSingleValueFieldError(scope=self.scope.alias, field=alias)

        return descriptor

    def _ensure_field_is_available(self, descriptor: descriptors.Descriptor[Subject], alias: str) -> descriptors.Descriptor[Subject]:
        if descriptors.options.Deprecated() in descriptor.options:
            self._warn_deprecated(exceptions.DeprecatedFieldError(scope=self.scope.alias, field=alias))

        if descriptors.options.NotSupported() in descriptor.options:
            self._warn_not_supported(exceptions.NotSupportedFieldError(scope=self.scope.alias, field=alias))

        return descriptor

    def _ensure_event_is_available(self, descriptor: descriptors.Descriptor[Subject], alias: str) -> descriptors.Descriptor[Subject]:
        if descriptors.options.Deprecated() in descriptor.options:
            self._warn_deprecated(exceptions.DeprecatedEventError(scope=self.scope.alias, event=alias))

        if descriptors.options.NotSupported() in descriptor.options:
            self._warn_not_supported(exceptions.NotSupportedEventError(scope=self.scope.alias, event=alias))

        return descriptor

    @staticmethod
    def _warn_deprecated(exception: Exception) -> None:
        warnings.warn(DeprecationWarning(exception))

    @staticmethod
    def _warn_not_supported(exception: Exception) -> None:
        warnings.warn(FutureWarning(exception))
