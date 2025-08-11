from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Collection
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from rmshared.sql import compiling

FF = TypeVar('FF')
L = TypeVar('L')
R = TypeVar('R')
E = TypeVar('E')
F = TypeVar('F')
V = TypeVar('V')


class IFilters(Generic[FF], metaclass=ABCMeta):
    @abstractmethod
    def make_tree_from_filter(self, filter_: F) -> compiling.ITree:
        ...


class ILabels(Generic[L], metaclass=ABCMeta):
    @abstractmethod
    def make_tree_from_labels(self, labels_: Collection[L], matcher: Matcher) -> compiling.ITree:
        ...

    @dataclass(frozen=True)
    class Matcher(metaclass=ABCMeta):
        ...

    @dataclass(frozen=True)
    class Match(Matcher):
        pass

    @dataclass(frozen=True)
    class MatchNot(Matcher):
        pass


class IRanges(Generic[R], metaclass=ABCMeta):
    @abstractmethod
    def make_tree_from_ranges(self, ranges_: Collection[R], matcher: Matcher) -> compiling.ITree:
        ...

    @dataclass(frozen=True)
    class Matcher(metaclass=ABCMeta):
        ...

    @dataclass(frozen=True)
    class Match(Matcher):
        pass

    @dataclass(frozen=True)
    class MatchNot(Matcher):
        pass


class IEvents(Generic[E], metaclass=ABCMeta):
    @abstractmethod
    def make_tree_from_event(self, event: E) -> compiling.ITree:
        ...


class IFields(Generic[F], metaclass=ABCMeta):
    @abstractmethod
    def make_tree_from_field(self, field: F) -> compiling.ITree:
        ...

    @abstractmethod
    def make_field_operations(self, field: F) -> IOperations:
        ...

    class IOperations(metaclass=ABCMeta):
        @abstractmethod
        def make_match_badge_operation(self) -> compiling.ITree:
            ...

        @abstractmethod
        def make_does_not_match_badge_operation(self) -> compiling.ITree:
            ...

        @abstractmethod
        def make_match_empty_operation(self) -> compiling.ITree:
            ...

        @abstractmethod
        def make_does_not_match_empty_operation(self) -> compiling.ITree:
            ...

        @abstractmethod
        def make_match_one_value_operation(self, expression: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_does_not_match_one_value_operation(self, expression: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_match_any_value_operation(self, expression: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_does_not_match_any_value_operation(self, expression: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_between_operation(self, min_value: compiling.ITree, max_value: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_not_between_operation(self, min_value: compiling.ITree, max_value: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_less_than_operation(self, value: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_less_than_or_equal_operation(self, value: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_more_than_operation(self, value: compiling.ITree) -> compiling.ITree:
            ...

        @abstractmethod
        def make_more_than_or_equal_operation(self, value: compiling.ITree) -> compiling.ITree:
            ...


class IValues(Generic[V], metaclass=ABCMeta):
    @abstractmethod
    def make_tree_from_value(self, value: V) -> compiling.ITree:
        ...


class IAssembler(Generic[FF, L, R, F, E, V], metaclass=ABCMeta):
    @abstractmethod
    def make_filters(self, labels_: ILabels[L], ranges_: IRanges[R]) -> IFilters[FF]:
        ...

    @abstractmethod
    def make_labels(self, fields_: IFields[F], values_: IValues[V]) -> ILabels[L]:
        ...

    @abstractmethod
    def make_ranges(self, fields_: IFields[F], values_: IValues[V]) -> IRanges[R]:
        ...

    @abstractmethod
    def make_fields(self) -> IFields[F]:
        ...

    @abstractmethod
    def make_events(self) -> IEvents[E]:
        ...

    @abstractmethod
    def make_values(self) -> IValues[V]:
        ...


class IComposite(Generic[FF, L, R, F, E, V], IFilters[FF], ILabels[L], IRanges[R], IEvents[E], IFields[F], IValues[V], metaclass=ABCMeta):
    ...


class IDescriptors(Generic[F, E], metaclass=ABCMeta):
    @abstractmethod
    def is_badge_field(self, field: F) -> bool:
        ...

    @abstractmethod
    def is_multi_value_field(self, field: F) -> bool:
        ...

    @abstractmethod
    def is_single_value_field(self, field: F) -> bool:
        ...

    @abstractmethod
    def get_field_alias(self, field: F) -> str:
        ...

    @abstractmethod
    def get_event_alias(self, event: E) -> str:
        ...
