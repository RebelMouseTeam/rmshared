from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Collection
from collections.abc import Sequence
from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Generic
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import variables
from rmshared.content.taxonomy.abc import Guid

F = TypeVar('F')
L = TypeVar('L')
R = TypeVar('R')
V = TypeVar('V')


class IContextManager(metaclass=ABCMeta):
    @abstractmethod
    def set_taxonomy_scope(self, scope: Scope) -> AbstractContextManager[None]:
        ...

    @dataclass(frozen=True)
    class Scope:
        alias: str
        entity: Type[Guid]  # TODO: Consider scopes other than entities (e.g. context)

    @abstractmethod
    def use_taxonomy_constant_filters(self) -> AbstractContextManager[None]:
        ...

    @abstractmethod
    def use_taxonomy_variable_filters(self, arguments: IArguments) -> AbstractContextManager[None]:
        ...

    class IArguments(metaclass=ABCMeta):
        @abstractmethod
        def resolve_reference_by_index(self, index: int) -> variables.Reference:
            ...

        @abstractmethod
        def resolve_reference_by_alias(self, alias: str) -> variables.Reference:
            ...

        @abstractmethod
        def get_yields(self, ref: variables.Reference) -> Collection[variables.arguments.Argument]:
            ...


class IContext(metaclass=ABCMeta):
    @property
    @abstractmethod
    def fields(self) -> IFields:
        ...

    @property
    @abstractmethod
    def filters(self) -> IFilters:
        ...

    @abstractmethod
    def set_scope(self, scope: IContextManager.Scope) -> IContext:
        ...

    @abstractmethod
    def use_constant_filters(self) -> IContext:
        ...

    @abstractmethod
    def use_variable_filters(self, arguments: IContextManager.IArguments) -> IContext:
        ...

    @abstractmethod
    def get_parent(self) -> IContext:
        ...


class IFields(metaclass=ABCMeta):
    @abstractmethod
    def resolve_id_field(self, alias: str) -> core.fields.Field:
        ...

    @abstractmethod
    def resolve_badge_system_field(self, alias: str) -> core.fields.Field:
        ...

    @abstractmethod
    def resolve_multi_value_system_field(self, alias: str) -> core.fields.Field:
        ...

    @abstractmethod
    def resolve_single_value_system_field(self, alias: str) -> core.fields.Field:
        ...

    @abstractmethod
    def resolve_custom_field(self, path: str) -> core.fields.Field:
        ...

    @abstractmethod
    def resolve_event(self, alias: str) -> core.events.Event:
        ...


class IFilters(Generic[F, L, R, V], metaclass=ABCMeta):
    @abstractmethod
    def resolve_reference_by_index(self, index: int) -> variables.Reference:
        ...

    @abstractmethod
    def resolve_reference_by_alias(self, alias: str) -> variables.Reference:
        ...

    @abstractmethod
    def make_constant_value(self, scalar: str | int | float) -> V:
        ...

    @abstractmethod
    def make_variable_value(self, alias: variables.Reference, index: int) -> V:
        ...

    @abstractmethod
    def make_return_badge_label(self, field: core.fields.Field) -> L:
        ...

    @abstractmethod
    def make_return_empty_label(self, field: core.fields.Field) -> L:
        ...

    @abstractmethod
    def make_return_value_label(self, field: core.fields.Field, value: V) -> L:
        ...

    @abstractmethod
    def make_return_between_range(self, field: core.fields.Field, min_value: V, max_value: V) -> F:
        ...

    @abstractmethod
    def make_return_less_than_range(self, field: core.fields.Field, value: V) -> F:
        ...

    @abstractmethod
    def make_return_more_than_range(self, field: core.fields.Field, value: V) -> F:
        ...

    @abstractmethod
    def make_return_any_label_filter(self, labels: Sequence[L]) -> F:
        ...

    @abstractmethod
    def make_return_no_labels_filter(self, labels: Sequence[L]) -> F:
        ...

    @abstractmethod
    def make_return_any_range_filter(self, ranges: Sequence[R]) -> F:
        ...

    @abstractmethod
    def make_return_no_ranges_filter(self, ranges: Sequence[R]) -> F:
        ...

    @abstractmethod
    def make_return_nothing(self) -> F:
        ...

    @abstractmethod
    def validate_return_filter(self, filter_: F) -> F:
        ...

    @abstractmethod
    def validate_switch_filter(self, filter_: F) -> F:
        ...
